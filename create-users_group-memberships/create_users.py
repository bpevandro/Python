import csv
import requests
import json
import getpass
import logging
import datetime
# Inputs
url = input("\nWhat's the instance's URL without \"https\"? ")
endpoint = '/rest/api/2/user'
auth_email = input("Auth email address: ")
auth_pass = getpass.getpass('Auth password: ')

# Read CSV file
with open('<file-here>.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	next(csvfile)
	for row in readCSV:
		print("\n")
		print('Attempting to create',row)

		email_address = row[3]
		name = row[1]+" "+row[2]
		username = row[0]

		# Make request
		data = {'displayName':name, 'emailAddress':email_address, 'name':username}
		response = requests.post("https://"+url+endpoint, headers={"content-type":"application/json"}, json=data, auth=(auth_email, auth_pass))

		# Print response
		if response.status_code == 201:
			print(response.status_code, 'User','"'+name+'"','was successfully created with email address','"'+email_address+'"','and username','"'+username+'".')

		elif response.status_code == 401:
			print(response.status_code, response.text)
			logFile = open('/Users/ebaginski/Desktop/users&group_membership/logs/users_log.txt', 'w+')
			logFile.write('%s %s' % (datetime.datetime.now(), str(response.status_code)))
			logFile.write(' ')
			logFile.write(response.text)
			logFile.write('\n')
			logFile.close()
			sys.exit()
		else:
			print(response.status_code, response.text)
			logFile = open('/Users/ebaginski/Desktop/users&group_membership/logs/users_log.txt', 'w+')
			logFile.write('%s %s' % (datetime.datetime.now(), str(response.status_code)))
			logFile.write(' ')
			logFile.write(response.text)
			logFile.write('\n')
			logFile.close()
