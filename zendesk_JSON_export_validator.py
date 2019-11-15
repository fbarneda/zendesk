"""
Convert JSON export (TICKETS) into a valid JSON file.

For more information:
https://support.zendesk.com/hc/en-us/articles/203662346-Exporting-data-to-a-JSON-CSV-or-XML-file-Professional-and-Enterprise-

USAGE: You will need to have a file called 'tickets.json' in the same directory where you run this script.
The script will generate a valid JSON file called 'export.json'.
"""
import tkinter as tk
from tkinter import filedialog

global output_file

def determine_export_type(input_file):

    with open(input_file, 'r') as first_input_file_line:
        first_input_file_line = first_input_file_line.readline()[0:99]

    tickets = ".zendesk.com/api/v2/tickets/" in first_input_file_line
    users = ".zendesk.com/api/v2/users/" in first_input_file_line
    organizations = ".zendesk.com/api/v2/organizations/" in first_input_file_line

    if tickets:
        export_type = "tickets"
    elif users:
        export_type = "users"
    elif organizations:
        export_type = "organizations"
    else:
        export_type = "invalid"

    return export_type


def validate_tickets(input_file):

    output_file = 'validated_tickets.json'

    with open(input_file, 'r') as all_input_file_lines:
        all_input_file_lines.readline()

        all_lines_with_comma = str()

        for line in all_input_file_lines:
            all_lines_with_comma += line[:-1] + ",\n"

    with open(output_file, 'w+') as write_output_file:
        write_output_file.writelines('{"tickets":[' + '\n' + all_lines_with_comma[:-3] + "\n}]}")
    print("Done, converted the file into a valid JSON file called '{}'.".format(output_file))

def main():

    root = tk.Tk()
    root.withdraw()
    input_file = filedialog.askopenfilename()

    export_type = determine_export_type(input_file)

    print(export_type)

    if export_type == "tickets":
        validate_tickets(input_file)


main()
# input_file = 'tickets.json'

#
# validate_full_json_export_tickets(input_file,output_file)
# print(determine_full_json_export_type(input_file))