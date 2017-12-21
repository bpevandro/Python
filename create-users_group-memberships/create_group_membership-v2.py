import csv
import requests
import json
import getpass
import logging
import datetime
import re
import sys

def createGroup(groupName):
	data_group = {'name':groupName}
	print('Attempting to create',groupName)
	response = requests.post("https://"+url+'/rest/api/2/group', headers={"content-type":"application/json"}, json=data_group, auth=(auth_email, auth_pass))
	if response.status_code == 201:
		print(response.status_code, 'Group','"'+groupName+'"','has been successfully created!')
		makeRequest(username, groupname)
	else:
		print(response.status_code, response.text)
	return

def makeRequest(username, groupname):
	# MAKE REQUEST
	data = {'name':username}
	print ('\nAttempting to add '+'"'+username+'"'+' into the '+'"'+groupname+'"'+' group..')
	response = requests.post("https://"+url+endpoint, headers={"content-type":"application/json"}, json=data, auth=(auth_email, auth_pass))

	# PRINT RESPONSE
	if response.status_code == 201:
		print(response.status_code, 'User','"'+username+'"','was added into the group '+groupname+' successfully!')

	elif "The group" in response.text and response.status_code == 404:
		print ('Group'+' "'+groupname+'" '+'does not exist in the target instance. Attempting to create it..')
		createGroup(groupname)

	elif response.status_code == 401:
		print(response.status_code, response.text)
		sys.exit()

	else:
		print(response.status_code, response.text)

	return response

# INPUTS
url = input("\nWhat's the instance's URL without \"https\"? ")
auth_email = input("Auth email address: ")
auth_pass = getpass.getpass('Auth password: ')

# READ CSV FILE
with open('group_memberships.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	next(csvfile)
	for row in readCSV:
		username = row[0]
		groupname = row[1]

		# BUG preventing creation using the endpoint below: https://jira.atlassian.com/browse/JRACLOUD-67118
		endpoint = '/rest/api/latest/group/user?groupname='+groupname.strip()
		#endpoint = '/admin/rest/um/1/user/group/direct?groupname='+groupname.strip()+'&username='+username.strip()

		# MAKE REQUEST
		response = makeRequest(username, groupname)
