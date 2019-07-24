import requests
import json
import os
import time


'''
Please edit "subdomain" with your subdomain
Please edit "username" with your Zendesk email address. Do not remove '/token'
Please edit "token" with a valid token from Admin > API > Token Access
'''

subdomain = 'xxxx'
user = 'xxxx/token'
token = 'xxxxxx'

url = 'https://' + subdomain + '.zendesk.com/api/v2/tickets'
print('>>> Accessing',url,'\n')

if os.path.exists('agents.csv'):
  os.remove('agents.csv')

page = 0
print("Entering loop now")

while url:

    r = requests.get(url, auth=(user, token))

# HTTP 200 Range
    if str(r.status_code)[0] == '2':

        page += 1

        print('Working on page number', page)

        json_data = r.json()

        my_file = open('agents.csv', 'a')

        for ticket in json_data['tickets']:

            my_file.write(json.dumps(ticket))
            my_file.write('\n')

        my_file.close()

        url = json_data['next_page']

# HTTP 400 Range
    elif str(r.status_code) == '403':

        print("HTTP 403 received. A 403 response means the server has determined the user or the account doesn’t have the required permissions to use the API.")
        break

    elif str(r.status_code) == '409':

        print("HTTP 409 received. A 409 response can indicate a merge conflict, but it often indicates a uniqueness constraint error in our database due to the attempted simultaneous creation of a resource. Try your API call again.\nIn general, the Zendesk API can handle concurrent API requests but the requests shouldn't be talking about the same resources such as the same requester. Serialize requests where possible.")
        break

    elif str(r.status_code) == '422':

        print("HTTP 422 received. A 422 response means that the content type and the syntax of the request entity are correct, but the content itself is not processable by the server. This is usually due to the request entity not being relevant to the resource that it's trying to create or update. Example: Trying to close a ticket that's already closed.")
        break

# HTTP 429
    elif str(r.status_code) == '429':

        print("HTTP 429 received. Waiting to retry again.")
        time_to_wait = int(r.headers['Retry-After'])
        time.sleep(time_to_wait)
        page -= 1
        continue

# HTTP 500 range
    elif str(r.status_code)[0] == '5':

        print("HTTP 500 range received. Printing request:\n")
        print(f"\n** HEADERS **\n {r.headers}")
        print(f"\n** CONTENT **\n {r.content}")
        break

    else:
        print("Looping back again.")
