# This script uses the Qualtrics API to import a survey into an user's account
# the permissions "Access API" is required for any target user
def createapitoken(userId,dataCenter,masterapi):
    baseUrl = "https://{0}.qualtrics.com/API/v3/users/{1}/apitoken".format(dataCenter,userId)
    headers = {
        'x-api-token': masterapi,
        }
    userId = userId.replace('\n','')
    response = requests.post(baseUrl, headers=headers)
    httpStatusCode = response.json()["meta"]["httpStatus"]
    if (httpStatusCode != "200 - OK"):
        response = requests.get(baseUrl, headers=headers)
        httpStatusCode = response.json()["meta"]["httpStatus"]
    if (httpStatusCode == "200 - OK"):
        apiToken = response.json()["result"]["apiToken"]
        print("apiToken status:",httpStatusCode)
    else:
        error = response.json()["meta"]["error"]["errorMessage"]
        print("apiToken status:",httpStatusCode,error)
        sys.exit()
    return apiToken
################################################################################
def importsurvey(surveyName,dataCenter,apiToken):
    baseUrl = "https://{0}.qualtrics.com/API/v3/surveys".format(dataCenter)
    headers = {
        "x-api-token": apiToken,
        }
    try:
        files = {
            'file': (surveyName, open(surveyName, 'rb'), 'application/vnd.qualtrics.survey.qsf')
            }
    except:
        print("File not found, please check that",surveyName,"is in working dirctory")
        sys.exit()
    data = { "name": surveyName }
    response = requests.post(baseUrl, files=files, data=data, headers=headers)
    httpStatusCode = response.json()["meta"]["httpStatus"]
    if (httpStatusCode == "200 - OK"):
        surveyId = response.json()["result"]["id"]
        print("import survey status:",httpStatusCode)
    else:
        error = response.json()["meta"]["error"]["errorMessage"]
        print("import survey status:",httpStatusCode,error)
        sys.exit()
    return surveyId


userId = input("Please enter the userID: ")
surveyName = input("Please enter the survey: ")
masterapi = ''
dataCenter = ''

apiToken = createapitoken(userId,dataCenter,masterapi)
importsurvey(surveyName,dataCenter,apiToken)
