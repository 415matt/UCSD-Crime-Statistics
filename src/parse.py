import pdfplumber
import unicodedata
import csv
from os import listdir
from os.path import isfile, join


def pdf_to_string(path):
    """Return the string representation of given PDF"""

    output_string = ""

    with pdfplumber.open(path) as pdf:
        # extract and append text from each page
        for curr_page in pdf.pages:
            output_string += curr_page.extract_text()

    # Normalize to replace non UTF-8 unicode from strings
    return unicodedata.normalize('NFKC', output_string).replace("‐", "-")


def parse(pdf_string):
    """Parses the given PDF string"""

    pdf_arr = pdf_string.splitlines()  # each line is an element in the list

    csv_rows = []  # stores each event[]
    i = 0
    while i < len(pdf_arr):

        # build event with required fields
        event = []
        while len(event) != 8 and i < len(pdf_arr):  # populate
            curr_line = pdf_arr[i]

            if "Date Reported" in curr_line:
                # append incident
                event.append(pdf_arr[i - 2])
                # append location
                event.append(pdf_arr[i - 1])
                # append Date Reported
                event.append(curr_line.replace("Date Reported ", ""))

            elif "Incident/Case#" in curr_line:
                event.append(curr_line.replace("Incident/Case# ", ""))

            elif "Date Occurred" in curr_line:
                event.append(curr_line.replace("Date Occurred ", ""))

            elif "Time Occurred" in curr_line:
                event.append(curr_line.replace("Time Occurred ", ""))

            elif "Summary" in curr_line:
                summary = ""

                if "Disposition" in pdf_arr[i + 1]:
                    summary = curr_line
                else:
                    # combine multi-line summaries
                    j = i
                    while "Disposition" not in pdf_arr[j]:
                        summary += pdf_arr[j]
                        j += 1

                event.append(summary.replace("Summary:", "").replace(" ", "", 1))

            elif "Disposition" in curr_line:
                event.append(curr_line.replace("Disposition: ", "").replace("UCSD POLICE DEPARTMENT ", ""))

            i += 1  # next line

        # add to be written to csv
        if len(event) == 8:
            csv_rows.append(event)

    return csv_rows


filepaths = listdir("../logs/")
files = []

for path in filepaths:
    files.append(parse(pdf_to_string("../logs/" + path)))


# Write to CSV
with open('main.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Heading row
    writer.writerow(["Incident", "Location", "Date Reported", "Incident/Case#",
                     "Date Occurred", "Time Occurred", "Summary", "Disposition"])

    for arr in files:
        for row in arr:
            writer.writerow(row)  # write the generated row to csv
