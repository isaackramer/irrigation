# irrigation

Final project for course data science course (semester 1/2018).

## Project Contents

### Code
This folder contains all the data, code, and output for the project. See subfolders.

#### Clean data
- TDR_data_clean.csv: All the variables from the soil sensors in a "clean" format. Removed "0.0" values and "-" from the original file and replaced them with nan. Proper datetime format used.
- TDR_data_clean_VWC.csv: Same data, but removed all variables except the volumetric water content (VWC).
- - TDR_data_clean_VWC.csv: Same as the above file, but only two days of data. Makes processing plots a bit faster...

#### Scripts
- data_clean.py: Cleans the data.
- facet.py: Plot basic time series, faceted by treatment
- more_analysis.py: Includes code for building a correlation matrix and resampling the data by hour/week/etc...


#### Output
- Please store your output here.


### Proposal
This folder contains the latex file we submitted as the project proposal.

### Random pdfs
This folder contains a few random PDFs with examples of how data science has been used in agriculture.

### description_of_data.md
This file contains a description of the raw data including the units and information from the research team.

### Readme.md
This file.

### useful_links.md
This file contains useful links. Feel free to add :)

### Site_Map.pdf
Map of the sensor locations.
