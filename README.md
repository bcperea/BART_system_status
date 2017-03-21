# Welcome to the BART_system_status Repository
## Brian Perea (c) 2017
This repository contains a simple analysis of BART system data collected
from March 2016 to March 2017.

# Files Contained in This Repository
* BART_data.csv : data table
* BART_data.py : Python code for making API calls
* BART_data.bat : Example Windows Batch file used for scheduling API calls
* 20170321_BART_data_analysis.ipynb : Jupyter Notebook summarizing data set
* LICENSE : Licensing information for repository contents

# Jupyter Notebook: Bay Area Rapid Transit (BART) Delays During Peak Hours

# The Data Set:

Data characterized in this repository was collected from the BART and
Open Weather Map APIs over the course of about a year from March 2016 to
March 2017. Data points were collected seven days a week, twice a day --
once in the morning at 8 AM and once in the evening at 5 PM. These hours
were selected to correspond to peak use hours, especially on weekdays.

The following features were collected:
* **date**: mm/dd/yyyy, date on which data was collected
* **description**: string, description of BART system status
* **elev_status**: string, description of elevator status in BART system
* **posted**: string, timestamp associated with API call
* **traincount**: count, number of active trains
* **type**: string, "DELAY" when delays on BART, else NaN
* **weather**: string, one-word description of weather conditions
