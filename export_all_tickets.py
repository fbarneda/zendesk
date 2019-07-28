"""
* Please edit "subdomain" with your subdomain
* Please edit "username" with your Zendesk email address. Do not remove '/token'
* Please edit "token" with a valid token from Admin > API > Token Access
"""

import requests, json, time, math


def reportDetails(r,page,num_tickets_to_export):
    page += 1
    print("[HTTP " + str(r.status_code) + "] - " + "Working on page number " + str(page) + "/" + str(math.ceil(num_tickets_to_export/100)), end='')
    print(" - RPM " + str(r.headers['X-Rate-Limit-Remaining']) + "/" + str(r.headers['X-Rate-Limit']))


def letsWait(wait_seconds):
    count_down = list(range(1, wait_seconds + 1))
    count_down.reverse()

    for num in count_down:
        print(str(num) + " seconds left")
        time.sleep(1)


subdomain = 'xxxxx'
username = ' xxxxxx@xxx.xxx/token'
token = 'xxxxxxxxxxx'
file_name = 'tickets.json'

# If you’re making several requests to the same host, the underlying TCP connection will be reused,
# which can result in a significant performance increase
session = requests.Session()

# We will be using the Tickets end-point
# For more info: https://developer.zendesk.com/rest_api/docs/support/tickets#list-tickets
url = 'https://' + subdomain + '.zendesk.com/api/v2/tickets.json'

print(f"\nEXPORT ALL MY TICKETS"
      f"\n**********************\n"
      f"\n* SUBDOMAIN: {subdomain}"
      f"\n* USER: {username}"
      f"\n* TOKEN: {token}"
      f"\n\n>>> Starting\n")

# Create file, open it and add a text needed to have a valid JSON file
# For more info: https://support.zendesk.com/hc/en-us/articles/203662346
my_file = open(file_name, 'w+')
my_file.write('{"tickets":[' + '\n')

page = 0
num_tickets_to_export = 0
while url:

    r = session.get(url, auth=(username, token))

    # HTTP 200 Range
    if str(r.status_code)[0] == '2':

        json_data = r.json()

        for ticket in json_data['tickets']:
            my_file.write('{"ticket": ' + json.dumps(ticket) + "},\n")  # This structure will create a valid JSON file

        num_tickets_to_export = json_data['count']
        url = json_data['next_page']

        # Printing details about the export, like number of pages left or API requests per minute used/left
        reportDetails(r,page,num_tickets_to_export)

        # Check if 'next_page' is None to finish export
        if url is None:

            print('\n>>> Finished')
            # Closing the file we are working on
            my_file.close()
            # read the file into a list of lines
            file_lines = open(file_name, 'r').readlines()
            # remove the ',' at the end of the last line and add a text to the end to make it a valid JSON
            new_last_line = (file_lines[-1][:-2] + "\n]}")
            file_lines[-1] = new_last_line
            #  write the modified last line back to the file
            open(file_name, 'w').writelines(file_lines)

            print(f"\n>>> All data saved in file: {file_name}")
            break

        else:
            continue


    # HTTP 400 Range
    elif str(r.status_code) == '401':

        print("\n>>> HTTP 401 received. Couldn't authenticate you. Please review SUBDOMAIN, USER and TOKEN.")
        break

    elif str(r.status_code) == '403':

        print(
            "\n>>> HTTP 403 received. A 403 response means the server has determined the user or the account doesn’t have the required permissions to use the API.")
        break

    elif str(r.status_code) == '409':

        print(
            "\n>>> HTTP 409 received. A 409 response can indicate a merge conflict, but it often indicates a uniqueness constraint error in our database due to the attempted simultaneous creation of a resource. Try your API call again.\nIn general, the Zendesk API can handle concurrent API requests but the requests shouldn't be talking about the same resources such as the same requester. Serialize requests where possible.")
        break

    elif str(r.status_code) == '422':

        print(
            "\n>>> HTTP 422 received. A 422 response means that the content type and the syntax of the request entity are correct, but the content itself is not processable by the server. This is usually due to the request entity not being relevant to the resource that it's trying to create or update. Example: Trying to close a ticket that's already closed.")
        break


    # HTTP 429
    # Best practices for avoiding rate limiting: https://develop.zendesk.com/hc/en-us/articles/360001074328
    elif str(r.status_code) == '429':

        print("\n>>> HTTP 429 received. Waiting to retry again.")

        try:

            time_to_wait = int(r.headers['Retry-After'])
            print("Received a 'Retry-After' of " + str(time_to_wait) + " seconds.\n")
            letsWait(time_to_wait)
            print("\nTrying again:")
            continue

        except:

            print("I could not see a header 'Retry-After'. Let's wait 1 min.")
            letsWait(60)
            continue


    # HTTP 500 range
    elif str(r.status_code)[0] == '5':

        print("\n>>> HTTP 500 range received. Printing request:\n")
        print(f"\n** HEADERS **\n {r.headers}")
        print(f"\n** CONTENT **\n {r.content}")
        break

    else:
        print(f"\n>>> ERROR\n {r.json()}")
        print(f"{r.status_code}")
        break

session.close()
