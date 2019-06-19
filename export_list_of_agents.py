    
import requests
import sys
import json
import os

'''
Please edit "subdomain" with your subdomain
Please edit "username" with your username. Do not remove 'token'
Please edit "token" with a valid token from Admin > API > Token Access
'''
subdomain = 'xxxxxx'
user = 'xxxxxxxx/token'
token = 'xxxxxxxxxx'

url = 'https://' + subdomain + '.zendesk.com/api/v2/users.json?role[]=agent&role[]=admin'
print('>>> Accessing',url,'\n')

if os.path.exists('agents.csv'):
  os.remove('agents.csv')

page = 0

while url:
    r = requests.get(url, auth=(user, token))
    if r.status_code != 200:
        print("ERROR: " + r.raise_for_status())
        break
    elif r.status_code == 200:
        page = page + 1
        print('Working on page number', page)
        json_data = r.json()
        file_ = open('agents.csv', 'a')
        for ticket in json_data['users']:
            file_.write(json.dumps(ticket['name']) + ", ")
            file_.write(json.dumps(ticket['email']) + ", ")
            file_.write(json.dumps(ticket['role']) + ", ")
            file_.write('\n')
        file_.close()
        url = json_data['next_page']
print('\nAll OK, data exported successfully.')
