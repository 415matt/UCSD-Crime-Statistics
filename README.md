# UCSD Crime Statistics
 
*An in-progress project to catalog and visualize the UC San Diego Police Department's Crime logs which are published [here](https://www.police.ucsd.edu/docs/reports/callsandarrests/Calls_and_Arrests.asp).*

## Why? ##
Despite containing a large amount of interesting and useful information, the daily crime bulletins published by UCPD are not easily searchable and only go back 60 days. The purpose of this project is to preserve the logs in an easily accessible format as a resource for students at UCSD. 

### Usage ###
`scraper.py` will download all the currently available .pdfs from the UCPD website and store them in `/logs/`

`parse.py` will generate a .csv with all the data from all of the pdf's stored in `/logs/`

<br>

#### Requirements #### 
+ [pdfplumber](https://pypi.org/project/pdfplumber/) 
+ [beautifulsoup](https://pypi.org/project/beautifulsoup4/)
