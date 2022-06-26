# UCSD Crime Statistics
 
*A project to catalog and visualize the UC San Diego Crime logs which are published [here](https://www.police.ucsd.edu/docs/reports/callsandarrests/Calls_and_Arrests.asp)*

### Usage ###
`scraper.py` will download all the currently available .pdfs from the UCPD website and store them in `/logs/.`

`parse.py` will generate a .csv file of all the crime logs stored in `/logs/.`



### Requirements ###
+ [pdfplumber](https://pypi.org/project/pdfplumber/)
+ [beautifulsoup](https://pypi.org/project/beautifulsoup4/)
