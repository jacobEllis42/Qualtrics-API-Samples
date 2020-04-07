import os, sys, requests
################################################################################
def responsefile():
    goodinput = 0
    createorcreated = input("Have the users been created?: (yes or no)")
    if createorcreated == "yes":
        while goodinput == 0:
            user_list = input("Please input the filename containing the user information: ")
            group = input("Would you like to add the existing users to a group? (yes or no)")
            if group == "yes":
                goodinput = 1
            elif group == "no":
                group = False
                goodinput = 1
            else:
                print("Input not recongized, please enter yes or no")
        while goodinput == 1:
            importSurvey = input("Would you like to import a survey to the existing users? (yes or no)")
            if importSurvey == "yes":
                surveyName = input("Please enter the filename of the QSF: ")
                goodinput = 2
            elif importSurvey == "no":
                data = False
                surveyName = False
                goodinput = 42
            else:
                print("Input not recongized, please enter yes or no")
        while goodinput == 2:
            importData = input("Would you like to import responses to the survey? (yes or no)")
            if importData == "yes":
                data = input("Please enter the filename of the CSV: ")
                goodinput = 42
            elif importData == "no":
                data = False
                goodinput = 42
            else:
                print("Input not recongized, please enter yes or no")
    elif createorcreated == "no":
        while goodinput == 0:
                user_list = input("Please input the filename containing the user information: ")
                goodinput = 1
        while goodinput == 1:
            group = input("Would you like to add the users to a group? (yes or no)")
            if group == "yes":
                goodinput = 2
            elif group == "no":
                group = False
                goodinput = 2
            else:
                print("Input not recongized, please enter yes or no")
        while goodinput == 2:
            importSurvey = input("Would you like to import a survey to the new users? (yes or no)")
            if importSurvey == "yes":
                surveyName = input("Please enter the filename of the QSF: ")
                goodinput = 3
            elif importSurvey == "no":
                surveyName = False
                data = False
                goodinput = 42
            else:
                print("Input not recongized, please enter yes or no")
        while goodinput == 3:
            importData = input("Would you like to import responses to the survy? (yes or no)")
            if importData == "yes":
                data = input("Please enter the filename of the CSV: ")
                goodinput = 42
            elif importData == "no":
                data = False
                goodinput = 42
            else:
                print("Input not recongized, please enter yes or no")

    return createorcreated, group, user_list, surveyName, data
################################################################################
def createuser(userinfo,dataCenter,apiToken):
    baseURL = "https://{0}.qualtrics.com/API/v3/users/".format(dataCenter)
    lang = userinfo[6]
    headers = {
        "x-api-token": apiToken,
        "Content-Type": "application/json"
        }

    data = {"username": userinfo[0],
        "firstName": userinfo[2],
        "lastName": userinfo[3],
        "userType": userinfo[4],
        "email": userinfo[5],
        "password": userinfo[1],
        "language": lang.replace('\n',''),
        }
    if len(userinfo) >= 8:
        data = {"username": userinfo[0],
            "firstName": userinfo[2],
            "lastName": userinfo[3],
            "userType": userinfo[4],
            "email": userinfo[5],
            "password": userinfo[1],
            "language": userinfo[6],
            "accountExpirationDate": userinfo[7]
            }

    response = requests.post(baseURL,json=data,headers=headers)
    httpStatusCode = response.json()["meta"]["httpStatus"]
    if (httpStatusCode == "200 - OK"):
        userId = response.json()["result"]["id"]
        print("user creation status:",httpStatusCode)
    else:
        error = response.json()["meta"]["error"]["errorMessage"]
        print("user creation status:",httpStatusCode,error)
        sys.exit()
    return userId
################################################################################
def addtogroup(userId,groupId,dataCenter,apiToken):
    groupId = groupId.replace('\n','')
    userId = userId.replace('\n','')
    baseUrl = "https://{0}.qualtrics.com/API/v3/groups/{1}/members".format(dataCenter, groupId)
    headers = {
        "x-api-token": apiToken,
        "Content-Type": "application/json"
        }
    data = {"userId": userId}
    response = requests.post(baseUrl, headers=headers,json = data)
    httpStatusCode = response.json()["meta"]["httpStatus"]
    if (httpStatusCode == "200 - OK"):
        print("user added to group status:",httpStatusCode)
    else:
        error = response.json()["meta"]["error"]["errorMessage"]
        print("user creation status:",httpStatusCode,error)
        sys.exit()
    return response
################################################################################
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
################################################################################
def importresponses(file,surveyId,dataCenter,apiToken):
    # define parameters
    if file == 0:
        sys.exit()
    baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/import-responses".format(dataCenter,surveyId)
    headers = {
        "x-api-token": apiToken,
        "content-type": "text/csv"
        }
    try:
        body = open(file, 'rb').read()
    except:
        print("File not found, please check to see that", file,"is in the working directory")
        sys.exit()
    response = requests.post(baseUrl,data=body,headers=headers)
    httpStatusCode = response.json()["meta"]["httpStatus"]
    if (httpStatusCode == "200 - OK"):
        progressId = response.json()["result"]["progressId"]
        #progress(progressId,surveyId)
        print("Import started")
    else:
        error = response.json()["meta"]["error"]["errorMessage"]
        print(httpStatusCode,error)
        sys.exit()
################################################################################
def progress(progressId,surveyId):
    baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/import-responses/{2}".format(dataCenter,surveyId,progressId)
    headers = {
        "x-api-token": apiToken
        }
    print('calling progress')
    progress = requests.get(baseUrl,headers=headers)
    print('progress called')
    print(progress.json())
    httpStatusCode = progress.json()["meta"]["httpStatus"]
    if (httpStatusCode == "200 - OK"):
        print("import responses status:",httpStatusCode)
        percentrecord = []
        percent = 0
        i = 0
        while (percent < 100):
            baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/import-responses/{2}".format(dataCenter,surveyId,progressId)
            headers = {
                "x-api-token": apiToken
                }
            progress = requests.get(baseUrl,headers=headers)
            httpStatusCode = progress.json()["meta"]["httpStatus"]
            if (httpStatusCode == "200 - OK"):
                percent = progress.json()["result"]["percentComplete"]
                percentrecord.append(percent)
                status = progress.json()["result"]["status"]
                if (i > 0) and  percentrecord[i] != percentrecord[i-1]:
                    print(" import progress:", percent)
            i += 1
        print(" import complete")
    else:
        errorMessage = progress.json()["meta"]["error"]["errorMessage"]
        print(httpStatusCode)
        print(errorMessage)
    #    sys.exit()
################################################################################
masterapi = ''
dataCenter = ''


createorcreated, group, user_list, surveyName, data = responsefile()
with open(user_list,'r') as usrlist:
    if createorcreated == "no":
        i = 0
        for row in usrlist:
            if i == 0:
                i += 1
            else:
                ii = i-1
                print("user number:",ii)
                list = row.split(",")
                userId = createuser(list,dataCenter,masterapi)
                print(userId)
                if group != False:
                    groupId = list[-1]
                    addtogroup(userId,groupId,dataCenter,masterapi)
                if surveyName != False:
                    apiToken = createapitoken(userId,dataCenter,masterapi)
                    surveyId = importsurvey(surveyName,dataCenter,apiToken)
                if data != False:
                    importresponses(data,surveyId,dataCenter,apiToken)
            i += 1
    if createorcreated == "yes":
            i = 0
            for row in usrlist:
                if i == 0:
                    i += 1
                else:
                    ii = i-1
                    print("user number:",ii)
                    list = row.split(",")
                    userId = list[0]
                    userId = userId.replace('\n','')
                    if group != False:
                        groupId = list[1]
                        addtogroup(userId,groupId,dataCenter,masterapi)
                    if surveyName != False:
                        apiToken = createapitoken(userId,dataCenter,masterapi)
                        surveyId = importsurvey(surveyName,dataCenter,apiToken)
                    if data != False:
                        importresponses(data,surveyId,dataCenter,apiToken)
                i += 1
