import sys
import requests
import json

from config import getApiKey, getCommentsApiUrl, getOutputExtension, getOutputFormatting, getCommentsCount
from formatting import parseData

# Gets the video id from the first arg
def getVideoId():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return ""

# Returns comments data from the API in json
def getCommentsData(url):
    req = requests.get(url)
    return req.json()

# Returns array of the json single comment records based on the videoId and the count.
def getComments(videoId, count):
    apiKey = getApiKey()
    apiUrl = getCommentsApiUrl()

    if(not apiKey or not apiUrl or not videoId):
        return []

    areMoreData = True
    comments = []
    token = ""
    urlForToken = apiUrl.replace("{api_key}", apiKey).replace("{video_id}", videoId)
    url = urlForToken.replace("{nextPageToken}", token)

    commentsCount = 0
    while(areMoreData and (commentsCount < count)):
        commentsData = getCommentsData(url)
        newComments = commentsData["items"]
        comments.extend(newComments)
        if("nextPageToken" in commentsData):
            token = commentsData["nextPageToken"]
            url = urlForToken.replace("{nextPageToken}", token)
            commentsCount = commentsCount + 100
        else:
            areMoreData = False
    return comments

# Writes the content to the file with the filename
def writeFile(filename, content):
    f = open("output_" + filename, "w", encoding="utf-8")
    f.write(content)
    f.close()

# Save the comments from the video with the videoId to the file named output_videoId. Comments are output from the GetComments().
def saveComments(videoId, comments):
    outExt = getOutputExtension()
    filename = videoId + "." + outExt
    fileFormatting = getOutputFormatting()

    if(outExt and fileFormatting):
        final = parseData(fileFormatting, comments)
        print('Writting file...')
        writeFile(filename, final)
    print("Done.")

# The main process
def main():
    videoId = getVideoId()
    comCount = getCommentsCount()
    if videoId:
        comments = getComments(videoId, comCount)
        saveComments(videoId, comments)
    else:
        print("Url of the video is missing. It should be the first arg.")

main()
