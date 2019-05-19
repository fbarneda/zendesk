import requests
import sys
import json
import os

subdomain = 'ZENDESK SUBDOMAIN'
url = 'https://' + subdomain + '.zendesk.com/api/v2/tickets.json'

print('>>> Accessing',url,'\n')

user = 'USERNAME/token'
password = 'TOKEN'

if os.path.exists('data.json'):
  os.remove('data.json')

page = 0

while url:
    r = requests.get(url, auth=(user, password))
    if r.status_code != 200:
        print("ERROR: " + r.raise_for_status())
    elif r.status_code == 200:
        page = page + 1
        print('Working on page number', page)
        json_data = r.json()
        file_ = open('data.json', 'a')
        for ticket in json_data['tickets']:
            file_.write(json.dumps(ticket))
            file_.write('\n')
        file_.close()
        url = json_data['next_page']
print('\nAll OK, data exported successfully.')
