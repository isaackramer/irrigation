# irrigation

Final project for course data science course (semester 1/2018).

## Project Contents

### Code
This folder contains all the data, code, and output for the project. See subfolders.

#### Clean data
- Good_Sensors_Only.csv: All the variables from the soil sensors in a "clean" format. Removed "0.0" values and "-" from the original file and replaced them with nan. Proper datetime format used. Removed sensors that appeared not to be working.
- Good_Sensors_Only.VWC.csv: Same data, but removed all variables except the volumetric water content (VWC).
- Irrigation.csv: Irrigation (millimeters of water) given to each of the treatment areas, by date.
- SWP.csv: The Stem Water Potential (SWP -- amount of water in the plant leaves) at different points during the measurement period.
- SWP_Long.csv: The Stem Water Potential (SWP -- amount of water in the plant leaves) at different points during the measurement period in a long format for easy plotting with other variables.
- sensor_meta.csv: Data about the slope and soil depth at each of the sensor locations.
##### Data with Bad Sensors
- TDR_data_clean.csv: All the variables from the soil sensors in a "clean" format. Removed "0.0" values and "-" from the original file and replaced them with nan. Proper datetime format used.
- TDR_data_clean_VWC.csv: Same data, but removed all variables except the volumetric water content (VWC).
- TDR_data_clean_VWC.csv: Same as the above file, but only two days of data. Makes processing plots a bit faster...

#### Scripts
- data_clean.py: Cleans the data.
- facet.py: Plot basic time series, faceted by treatment
- facet_with_irrigation.py: Plot basic time series, faceted by treatment. Also plots irrigation and SWP data.
- more_analysis.py: Includes code for building a correlation matrix and resampling the data by hour/week/etc...
- distances.py: Noam?


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

### Goals.md
Describes short and long-term project goals.
