import requests, sys

def prompt():
    goodinput = 0
    while goodinput == 0:
        userId = input("Please input the userId: ")
        delAll = input("Would you like to delete all surveys in the user(s) account?")
        if delAll == "yes":
            delAll = True
            goodinput = 42
            surveyId = False
        elif delAll == "no":
            delAll = False
            surveyId = input("Please enter the surveyId: ")
            goodinput = 42
        else:
            print("Input not recongized. Please answer yes or no")
    return userId, delAll, surveyId

def listsurvey(apiToken,dataCenter):
    baseUrl = 'https://{0}.qualtrics.com/API/v3/surveys'.format(dataCenter)
    headers = {
        'X-API-TOKEN': apiToken,
        }

    response = requests.get(baseUrl, headers=headers)
    httpStatusCode = response.json()["meta"]["httpStatus"]
    if (httpStatusCode == "200 - OK"):
        surveys = response.json()
        survey_list = surveys["result"]["elements"]
    else:
        error = response.json()["meta"]["error"]["errorMessage"]
        print("list survey status:",httpStatusCode,error)
        sys.exit()
    return survey_list

def delsurvey(apiToken,surveyId):
    baseUrl = 'https://{0}.qualtrics.com/API/v3/surveys/{1}'.format(dataCenter,surveyId)
    headers = {
        'X-API-TOKEN': apiToken,
        }

    response = requests.delete(baseUrl, headers=headers)
    httpStatusCode = response.json()["meta"]["httpStatus"]
    if (httpStatusCode == "200 - OK"):
        print(surveyId,"deleted")
    else:
        error = response.json()["meta"]["error"]["errorMessage"]
        print("survey failed to delete:",httpStatusCode,error)
        sys.exit()

def delall(apiToken,userId):
    surveys = listsurvey(apiToken,dataCenter)
    for el in surveys:
        surveyId = el["id"]
        ownerId = el["ownerId"]
        if ownerId == userId:
            delsurvey(apiToken,surveyId)
        else:
            print("not the survey owner of",surveyId)


apiToken = ''
dataCenter = ''

userId,delAll, surveyId = prompt()
if delAll == True:
    delall(apiToken,userId)
elif delAll == False:
    delsurvey(apiToken,surveyId)
