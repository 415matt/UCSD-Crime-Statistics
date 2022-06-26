import os
import requests
from bs4 import BeautifulSoup


def download_pdf(url, filename):
    """Downloads the specified PDF from URL"""
        
    # request and write content
    response = requests.get(url)
    with open("logs/" + filename, 'wb') as f:
        f.write(response.content)


# scrape dropdown values from UCPD's website
html_doc = requests.get("https://www.police.ucsd.edu/docs/reports/callsandarrests/Calls_and_Arrests.asp").content
soup = BeautifulSoup(html_doc, 'html.parser')

pdf_list = [option.get('value') for option in soup.find_all('option')]

# folder to store pdf logs
if not os.path.exists("logs/"):
    os.mkdir("logs/")

# download pdf's from dropdown
for pdf in pdf_list:
    filename = pdf.split('/')[-1]
    url = "https://www.police.ucsd.edu/docs/reports/callsandarrests/" + pdf

    if not os.path.exists("logs/" + filename):
        download_pdf(url, filename)
