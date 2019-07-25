"""
* Please edit "subdomain" with your subdomain

* Please edit "username" with your Zendesk email address. Do not remove '/token'

* Please edit "token" with a valid token from Admin > API > Token Access

"""

import requests, json, time


def letsWait(wait_seconds):

    count_down = list(range(1,wait_seconds+1))
    count_down.reverse()

    for num in count_down:

        print(str(num) + " seconds left")
        time.sleep(1)


subdomain = 'XXXXX'
user = 'XXXX@XXX.XXX/token'
token = 'XXXXX'
file_name = 'agents.csv'

url = 'https://' + subdomain + '.zendesk.com/api/v2/users.json?role[]=agent&role[]=admin'
print('\n>>> EXPORTING from: ',url,'\n')

# Create file
my_file = open(file_name, 'w+')
my_file.write('"ID","NAME","EMAIL","ROLE","CREATED_AT","UPDATED_AT"\n')

page = 0

while url:

    r = requests.get(url, auth=(user, token))

# HTTP 200 Range
    if str(r.status_code)[0] == '2':

        page += 1

        print("Working on page number " + str(page))

        json_data = r.json()

        for user in json_data['users']:

            print(json.dumps(user))

            my_file.write(json.dumps(user['id']) + ", ")
            my_file.write(json.dumps(user['name']) + ", ")
            my_file.write(json.dumps(user['email']) + ", ")
            my_file.write(json.dumps(user['role']) + ", ")
            my_file.write(json.dumps(user['created_at']) + ", ")
            my_file.write(json.dumps(user['updated_at']) + "\n")

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

        try:

            time_to_wait = int(r.headers['Retry-After'])
            print("Received a 'Retry-After' of " + str(time_to_wait) + " seconds.")
            letsWait(time_to_wait)
            continue

        except:

            print("I could not see a header 'Retry-After'. Let's wait 1 min.")
            letsWait(60)
            continue


# HTTP 500 range
    elif str(r.status_code)[0] == '5':

        print("HTTP 500 range received. Printing request:\n")
        print(f"\n** HEADERS **\n {r.headers}")
        print(f"\n** CONTENT **\n {r.content}")
        break


    else:

        print("Something went wrong, please review the information entered.")


# Closing the file we are working on
my_file.close()

print("\n>>> DONE - Export Finished OK")
