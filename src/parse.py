#TODO: parse arrest data

from os import listdir
from os.path import isfile, join

import pdfplumber
import unicodedata
import csv


class Event:
    def __init__(self):
        self.incident = ""
        self.location = ""
        self.dt_reported = ""
        self.case_num = ""
        self.dt_occured = ""
        self.time_occured = ""
        self.summary = ""
        self.disposition = ""
    
    def to_list(self):
        return [self.incident, 
                self.location, 
                self.dt_reported, 
                self.case_num, 
                self.dt_occured, 
                self.time_occured, 
                self.summary, 
                self.disposition]


class Arrest:
    def __init__(self):
        self.date = ""
        self.time = ""
        self.name = ""
        self.dob = ""
        self.description = ""
        self.occupation = ""
        self.charge = ""


def pdf_to_string(path):
    """Return the string representation of given PDF"""

    output_string = ""

    # extract and append text from each page
    with pdfplumber.open(path) as pdf:
        for curr_page in pdf.pages:
            output_string += curr_page.extract_text()

    # Normalize to replace non UTF-8 unicode from strings
    return unicodedata.normalize('NFKC', output_string).replace("‐", "-")

def parse(pdf_string):
    """Parses the given string, returns a list of event objects"""

    # create and store Event objects
    event = Event()
    pdf_events = []

    # iterate through each line in the pdf
    pdf_arr = pdf_string.splitlines()
    for i in range(len(pdf_arr)):

        curr_line = pdf_arr[i]

        if "Date Reported" in curr_line:
            # incident
            event.incident = str(pdf_arr[i - 2])
            # location
            event.location = str(pdf_arr[i - 1])
            # date reported
            curr_line = curr_line.replace("Date Reported ", "")
            event.dt_reported = curr_line

        elif "Incident/Case#" in curr_line:
            curr_line = curr_line.replace("Incident/Case# ", "")
            event.case_num = curr_line

        elif "Date Occurred" in curr_line:
            curr_line = curr_line.replace("Date Occurred ", "")
            event.dt_occured = curr_line

        elif "Time Occurred" in curr_line:
            curr_line = curr_line.replace("Time Occurred ", "")
            event.time_occured = curr_line

        elif "Summary" in curr_line:
            summary = ""

            if "Disposition" in pdf_arr[i + 1]:
                summary = curr_line
            # combine multi-line summaries
            else:
                j = i
                while "Disposition" not in pdf_arr[j]:
                    summary += pdf_arr[j]
                    j += 1

            summary = summary.replace("Summary:", "").replace(" ", "", 1)
            event.summary = summary

        elif "Disposition" in curr_line:
            curr_line = curr_line.replace("Disposition: ", "").replace("UCSD POLICE DEPARTMENT ", "")
            event.disposition = curr_line

            # add event object to the list & reset
            pdf_events.append(event)
            event = Event()
            
    return pdf_events


filepaths = listdir("logs/")

# Write to CSV
with open('main.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Heading row
    writer.writerow(["Incident", "Location", "Date Reported", "Incident/Case#",
                     "Date Occurred", "Time Occurred", "Summary", "Disposition"])

    # iterate through each pdf and add their events each as a row in csv
    for filepath in filepaths:
        events = parse(pdf_to_string("logs/" + filepath))

        for event in events:
            writer.writerow(event.to_list())
