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

file = input("Please enter the filename (format must be CSV): ")
surveyId = input("Please enter the surveyId associated with the responses: ")
dataCenter = ''
apiToken = '' 
