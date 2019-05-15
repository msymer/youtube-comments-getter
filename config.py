import json

CONFIG_FILENAME = "config.json"
COMMENTS_APIKEY_KEY = "apiKey"
FORMATTING_KEY = "formatting"
OUTPUT_FILE_EXT_KEY = "outputExtension"
COMMENTS_API_URL_KEY = "commentsApiUrl"
COMMENTS_COUNT_KEY = "commentsCount"

# Gets content of the config file in json
def getContent():
    f = open(CONFIG_FILENAME, "r")
    return json.loads(f.read())

# Gets API key from the config file
def getApiKey():
    content = getContent()
    if(COMMENTS_APIKEY_KEY in content):
        return content[COMMENTS_APIKEY_KEY]
    else:
        print('API key is not in the config file.')
        return ""

# Gets formatting style from the config file
def getOutputFormatting():
    content = getContent()
    if(FORMATTING_KEY in content):
        return content[FORMATTING_KEY]
    else:
        print('Formatting is not in the config file.')
        return ""

# Gets output file extension from the config file
def getOutputExtension():
    content = getContent()
    if(OUTPUT_FILE_EXT_KEY in content):
        return content[OUTPUT_FILE_EXT_KEY]
    else:
        print('Output file extension is not in the config file.')
        return ""

# Gets comments api url from the config file
def getCommentsApiUrl():
    content = getContent()
    if(COMMENTS_API_URL_KEY in content):
        return content[COMMENTS_API_URL_KEY]
    else:
        print('Comments api url is not in the config file.')
        return ""

# Gets comments count from the config file
def getCommentsCount():
    content = getContent()
    if(COMMENTS_COUNT_KEY in content):
        return content[COMMENTS_COUNT_KEY]
    else:
        print('Comments count is not in the config file.')
        return ""