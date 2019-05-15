import json

RECORD_SECTION = "<RR>"
SEPARATOR_SECTION = "<SS>"
MAIN_COMMENT_TAG = "<CMT>"
REPLY_COMMENT_TAG = "<RCMT>"
AUTHOR_TAG = "<ATH>"
LIKES_TAG = "<RAT>"
NEWLINE_TAG = "<NL>"
DATE_TAG = "<DAT>"
REPLIES_TAG = "<REP>"
ID_TAG = "<ID>"
PARENT_TAG = "<PAR>"

# Returns array of all the record format sections. [ section, section...]
def getRecordFormmattingSections(formatting):
    rSecIndexes = getIndexRecordSections(formatting)
    result = []
    for rec in rSecIndexes:
        substr = formatting[rec[0] + len(RECORD_SECTION) : rec[1] - len(RECORD_SECTION)]
        result.append(substr)
    return result

# Returns array of indexes of all the record format sections. [[start, end], [start, end]...]
def getIndexRecordSections(formatting):
    result = []
    run = True
    lastIndex = 0
    endSpace = len(RECORD_SECTION) * 2
    while run:
        record = []
        start = formatting.find(RECORD_SECTION, lastIndex)
        if(start == -1):
            print("Incorrect formatting.")
            return result
        lastIndex = start + len(RECORD_SECTION)
        end = formatting.find(RECORD_SECTION, lastIndex) + len(RECORD_SECTION)
        lastIndex = end
        if(end == -1):
            print("Incorrect formatting.")
            return result
        result.append([start, end])
        if(len(formatting) <= lastIndex + endSpace):
            run = False
    return result

# Returns text created from the record format section (recordFormatting) and the input comments from the API in json
def parseRecord(recordFormatting, data):
    mainComment = ""
    replyComment = ""
    author = ""
    likes = ""
    date = ""
    replies = ""
    idc = ""
    parent = ""

    if ("snippet" in data) and ("topLevelComment" in data["snippet"]) and ("snippet" in data["snippet"]["topLevelComment"]):
        cmt = data["snippet"]["topLevelComment"]["snippet"]
        if("authorDisplayName" in cmt):
            author = cmt["authorDisplayName"]

        if("textDisplay" in cmt):
            if("parentId" in cmt):
                parent = cmt["parentId"]
                replyComment = cmt["textDisplay"].replace("\n", " ")
            else:
                mainComment = cmt["textDisplay"].replace("\n", " ")

        if("likeCount" in cmt):
            likes = cmt["likeCount"]

        if("updatedAt" in cmt):
            date = cmt["updatedAt"]

    if("id" in data):
        idc = data["id"]
    
    if("snippet" in data) and ("totalReplyCount" in data["snippet"]):
        replies = data["snippet"]["totalReplyCount"]
    
    result = recordFormatting.replace(MAIN_COMMENT_TAG, mainComment).replace(REPLY_COMMENT_TAG, replyComment).replace(AUTHOR_TAG, author).replace(LIKES_TAG, str(likes))
    result = result.replace(DATE_TAG, date).replace(REPLIES_TAG, str(replies)).replace(ID_TAG, idc).replace(PARENT_TAG, parent)
    return result

# Gets the indexes of the seperator format section in the record format section (recordFormatting). Returns [start, end]
def getIndexesRecordSeparator(recordFormatting):
    result = []
    start = recordFormatting.find(SEPARATOR_SECTION)
    if(start == -1):
        print("Incorrect formatting.")
        return result
    end  = recordFormatting.find(SEPARATOR_SECTION, start + len(SEPARATOR_SECTION))+ len(SEPARATOR_SECTION)
    if (end == -1) or (end > len(recordFormatting)):
        print("Incorrect formatting.")
        return result
    result.append(start)
    result.append(end)
    return result

# Gets the separator format section from the record format section (recordFormatting).
def getRecordSeparator(recordFormatting):
    inx = getIndexesRecordSeparator(recordFormatting)
    if(len(inx) < 2):
        return ""
    separator = recordFormatting[inx[0] + len(SEPARATOR_SECTION) : inx[1] - len(SEPARATOR_SECTION)]
    return separator

# Parse the data to the format. Data is in json. The data is parsed based on the json format from API response (15.5.2019)
def parseData(formatting, data):
    print("Preparing formatting...")
    recSecIndexes = getIndexRecordSections(formatting)
    parts = []
    lastIndex = 0
    for inx in recSecIndexes:
        parts.append(formatting[lastIndex : inx[0]])
        lastIndex = inx[1]
    parts.append(formatting[lastIndex : len(formatting)])

    recordSections = getRecordFormmattingSections(formatting)
    separatorIndexes = []
    separators = []
    for s in recordSections:
        index = getIndexesRecordSeparator(s)
        sep = getRecordSeparator(s)
        separatorIndexes.append(index)
        separators.append(sep)

    records = []
    for i in range(len(recordSections)):
        recordSections[i] = recordSections[i][:separatorIndexes[i][0]] + recordSections[i][separatorIndexes[i][1]:]
        records.append([])

    print("Parsing data...")
    for record in data:
        for i in range(len(recordSections)):
            res = parseRecord(recordSections[i], record)
            records[i].append(res)

    sections = []
    for i in range(len(records)):
        sec = separators[i].join(records[i])
        sections.append(sec)
    
    final = ""

    for i in range(len(parts)-1):
        final += parts[i]
        final += sections[i]
    final += parts[len(parts)-1]
    final = final.replace(NEWLINE_TAG, "\n")
    return final
