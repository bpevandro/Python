import csv
import requests
import json
import getpass
import logging
import datetime
import re
from datetime import datetime, timedelta

def getTime(timeMin):
    minutes = timedelta(minutes=timeMin)
    d = datetime(1,1,1) + minutes
    
    return d.day-1, d.hour, d.minute


# Inputs
url = input("\nWhat's the instance's URL without \"https\"? ")
work_hours = input("\nWorking hours per day? (This is configured at '<instance>/secure/admin/TimeTrackingAdmin.jspa)': ")
work_hours = int(work_hours)
work_hours = work_hours * 60
issue = input("\nWhat's the issue you want to GET the worklogs from? ")
endpoint = '/rest/api/2/issue/'+issue
auth_email = input("\nAuth email address: ")
auth_pass = getpass.getpass('\nAuth password: ')

# Make Request
response = requests.get("https://"+url+endpoint, headers={"content-type":"application/json"}, auth=('epereira@atlassian.com', 'qjZt1Y6NXhZACv0swF9HD6B4'))

data = response.json()

# Print Time Tracking information, such as Remaining Estimate
print("\ntimetracking: " + str(data['fields']['timetracking']))
print("\n")

# It saves into "json_worklog_obj" the worklogs object
json_worklog_obj = data['fields']['worklog']['worklogs']

i = 0
users = {}

# Iterates through "json_worklog_obj" to get the users as well as the time spent by them
for x in json_worklog_obj:
    timeSpent_final = 0
    print("User: " + str(json_worklog_obj[i]['author']['name']))
    print("TimeSpent: " + str(json_worklog_obj[i]['timeSpent']))

    # It stores the author's name into "user"
    user = str(json_worklog_obj[i]['author']['name'])

    # It stores the author's time spent into "timeSpent"
    timeSpent = str(json_worklog_obj[i]['timeSpent'])

    timeSpent_re = re.search(r'([0-9]+d)?( )?([0-9]+h)?( )?([0-9]+m)?( )?', timeSpent, re.M|re.I)
    group_1 = timeSpent_re.group(1)
    group_3 = timeSpent_re.group(3)
    group_5 = timeSpent_re.group(5)

    if group_1 is not None:
        group_1_re = re.search(r'[0-9]+', group_1, re.M|re.I)
        group_1_re = int(group_1_re.group(0))
        group_1_re = group_1_re * work_hours
        timeSpent_final = timeSpent_final + group_1_re

    if group_3 is not None:
        group_3_re = re.search(r'[0-9]+', group_3, re.M|re.I)
        group_3_re = int(group_3_re.group(0))
        group_3_re = group_3_re * 60
        timeSpent_final = timeSpent_final + group_3_re

    if group_5 is not None:
        group_5_re = re.search(r'[0-9]+', group_5, re.M|re.I)
        group_5_re = int(group_5_re.group(0))
        timeSpent_final = timeSpent_final + group_5_re

    flag = 0

    # Iterates through users dictionary to see if the current user retrieve from the JSON exists already
    for user_loop in users:

        # If it does exist, get the existing value and sum up with the new value retrieve from JSON
        if user == user_loop:
             total = users.get(user) + timeSpent_final
             users[user] = total
             flag = 1

    # Saving it as {"author": "timeSpent"}
    if flag != 1:
        users[user] = timeSpent_final

    i+=1

for key, value in users.items():

    print("\nUser " + "\"" + str(key) + "\"" + " has logged a total amount of " + str(value) + " minutes.")
