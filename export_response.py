import requests, zipfile, io
def createresponseexport(fileFormat,apiToken,dataCenter,surveyId):
    headers = {
        'X-API-TOKEN': apiToken,
        'Content-Type': 'application/json',
        }
    data = {"format": fileFormat,
            "startDate":'2016-04-01T07:31:43Z',
            "endDate":'2020-04-01T07:31:43Z',
            #"questionIds":["QID7", "QID6", "QID5", "QID4","QID3","QID2","QID1"],
            }
    baseUrl = 'https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses'.format(dataCenter,surveyId)
    response = requests.post(baseUrl, headers=headers, json=data)
    progressId = response.json()["result"]["progressId"]
    return progressId
def getresponseprogress(apiToken,dataCenter,surveyId,progressId):
    headers = {
        'X-API-TOKEN': apiToken,
        'Content-Type': 'application/json',
        }
    baseUrl = 'https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/{2}'.format(dataCenter,surveyId,progressId)
    response = requests.get(baseUrl, headers=headers)
    progress = response.json()["result"]["percentComplete"]
    while progress < 100.0:
        response = requests.get(baseUrl, headers=headers)
        progress = response.json()["result"]["percentComplete"]
    fileId = response.json()["result"]["fileId"]
    return fileId

def getresponsefile(apiToken,dataCenter,surveyId,fileId):
    headers = {
    'X-API-TOKEN': apiToken,
    'Content-Type': 'application/json',
        }
    baseUrl = 'https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/{2}/file'.format(dataCenter,surveyId,fileId)
    response = requests.get(baseUrl, headers=headers)
    zipfile.ZipFile(io.BytesIO(response.content)).extractall("test")
    print('Complete')




surveyId = input('Please enter the surveyId')
fileFormat = input('Please enter the desired file format (json, xml, or csv): ' )
apiToken = ''
dataCenter = ''


progressId = createresponseexport(fileFormat,apiToken,dataCenter,surveyId)
fileId = getresponseprogress(apiToken,dataCenter,surveyId,progressId)
getresponsefile(apiToken,dataCenter,surveyId,fileId)
