'''
API call to Production LRS 
'''
#Import tincan and json.
from tincan.remote_lrs import RemoteLRS
import json

#Configured variables from https://cloud.scorm.com/sc/user/LRSView
appID = 'JOFY1QJRK6'
secretKey = '5k1lIYbpBqiyWDSvzRksGRKmeRDQEJivmeFuDqyO'
endpoint = f'https://cloud.scorm.com/lrs/{appID}/'

#Prepare API request with tincan.RemoteLRS, which hashes and encrypts username and password. Store response in variable.
rlrs = RemoteLRS(endpoint=endpoint, username=appID, password=secretKey)

#Send the API request with query. Convert response data to json and store in a variable.
raw_data = json.loads(rlrs.query_statements(query={'since':'2022-01-01T12:00:00.000'}).data)

#Write json to file.
with open('../data/statements.json', 'w') as statements:
    json.dump(raw_data, statements)