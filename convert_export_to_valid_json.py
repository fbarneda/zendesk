"""
Convert JSON export into a valid JSON file.
For more info:
https://support.zendesk.com/hc/en-us/articles/203662346-Exporting-data-to-a-JSON-CSV-or-XML-file-Professional-and-Enterprise-
"""

from os import path


def main():

    # Check if we have a file tickets.json created, otherwise we cannot work.
    if path.exists("tickets.json"):

        # Files used
        # You will need to have a file called 'tickets.json' in the same folder as this script
        input_file = 'tickets.json'
        output_file = 'export.json'

        # Create file, open it and add a text needed to have a valid JSON file
        write_output_file = open(output_file, 'w+')
        write_output_file.write('{"tickets":[' + '\n')

        print("\n>>> Reading {}".format(input_file))

        # read the file into a list of lines
        all_input_file_lines = open(input_file, 'r').readlines()
        print("\n>>> Adding a comma at the end of each line and text needed to have a valid JSON file")

        # Go line per line and add a ',' at the end of each line
        all_lines_with_comma = str()
        for line in all_input_file_lines:
            all_lines_with_comma += line[:-1] + ",\n"

        # Add a text needed to have a valid JSON file
        # Write the new lines with the comma and close file
        write_output_file.writelines(all_lines_with_comma[:-2] + "\n}]}")
        write_output_file.close()

        print("\n>>> OK - All data saved in: {}".format(output_file))

    else:

        message = """
        >>> You do not have a tickets.json in the folder where you are running the script.
        
        >>> Please create a file tickets.json and try again.
        """
        print(message)


if __name__ == "__main__":
    main()
