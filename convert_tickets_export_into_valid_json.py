"""
Convert JSON export (TICKETS) into a valid JSON file.

For more information:
https://support.zendesk.com/hc/en-us/articles/203662346-Exporting-data-to-a-JSON-CSV-or-XML-file-Professional-and-Enterprise-

USAGE: You will need to have a file called 'tickets.json' in the same directory where you run this script.
The script will generate a valid JSON file called 'export.json'.
"""


def main():
    
    input_file = 'tickets.json'
    output_file = 'export.json'

    with open(input_file, 'r') as all_input_file_lines:
        all_input_file_lines.readline()

        all_lines_with_comma = str()

        for line in all_input_file_lines:
            all_lines_with_comma += line[:-1] + ",\n"

    with open(output_file, 'w+') as write_output_file:
        write_output_file.writelines('{"tickets":[' + '\n' + all_lines_with_comma[:-3] + "\n}]}")


if __name__ == "__main__":
    main()
