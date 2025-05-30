import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Clear workspace
# Not directly applicable in Python

# Functionality Description:
# Wind speeds are logged at a 5-second interval. This script addresses missing data gaps by 
# filling them with NaN values, enabling the combination of SPL data with MET data in AMT.
# The script can handle up to three data gaps during a standard 30-day monitoring period.

############################# START USER INPUT #######################
site_name = "your_site_code" # Typically four letter park code and 3 digit numeric code. Sample dataset ex. (YOSE013)
deploy = "your_deployment_date" # Typically 8 digits representing the day of deployment in YYYYMMDD. Sample dataset ex. (20240618)

# Missing data input
sdate1 = ""  # Start date
edate1 = ""    # End date

sdate2 = ""     # Start date
edate2 = ""   # End date

sdate3 = ""                     # Start date (input if applicable)
edate3 = ""                     # End date (input if applicable)

############## END USER INPUT ############################################################

# Create gap intervals and dataframes
def create_gap(sdate, edate):
    start_date = pd.to_datetime(sdate, format='%m/%d/%Y %H:%M:%S', utc=True)
    end_date = pd.to_datetime(edate, format='%m/%d/%Y %H:%M:%S', utc=True)
    return pd.DataFrame({'x': pd.date_range(start=start_date, end=end_date, freq='5S')})

gap1 = create_gap(sdate1, edate1)
gap2 = create_gap(sdate2, edate2)
gap3 = create_gap(sdate3, edate3) if sdate3 and edate3 else pd.DataFrame()

# Choose files (mocking interaction for automation)
Files = choose.files() # would be replaced with a specific file listing in Python.
# For example:
import glob
# Files = glob.glob("*.csv")  # Assuming .csv files in the current directory.

# Read wind data into a single dataframe
wind_files_df = [pd.read_csv(file, usecols=[0, 1, 2, 3], skiprows=1) for file in Files]
data = pd.concat(wind_files_df, ignore_index=True)

# Combine time zone extraction
tzhobo = Files[0].split('(')[-1].split(')')[0][6:8]

# Assign appropriate column names
data.columns = ["#", f"Date-Time ({tzhobo})", "Ch:1 - WindSpd - Speed  (m_s)", "Ch:1 - WindSpd - SpeedMax : Max (m_s)"]

# Create a numeric date/time field for sorting later
data['sort'] = pd.to_numeric(pd.to_datetime(data[f"Date-Time ({tzhobo})"], utc=True))

# Combine all gap data into a single dataframe
gapdata = pd.concat([gap1, gap2, gap3], ignore_index=True)

# Create new columns to match incoming "real data"
gapdata['x1'] = ""
gapdata['x2'] = 0.0000
gapdata['x3'] = 0.0000
gapdata = gapdata.reindex(columns=["x1", "x", "x2", "x3"])  # Ensure x1 is the first column

# Rename columns to match incoming data names
gapdata.columns = ["#", f"Date-Time ({tzhobo})", "Ch:1 - WindSpd - Speed  (m_s)", "Ch:1 - WindSpd - SpeedMax : Max (m_s)"]

# Create a numeric date/time field for sorting combined data frames later
gapdata['sort'] = pd.to_numeric(pd.to_datetime(gapdata[f"Date-Time ({tzhobo})"], utc=True))

# Reformat date/time field to match real data from HOBO loggers
gapdata[f"Date-Time ({tzhobo})"] = gapdata[f"Date-Time ({tzhobo})"].dt.strftime('%m/%d/%Y %H:%M:%S')

# Create log of gap dates
startdates = [sdate1, sdate2, sdate3] if sdate3 else [sdate1, sdate2]
enddates = [edate1, edate2, edate3] if edate3 else [edate1, edate2]
missing_observations = [len(gap1), len(gap2), len(gap3)] if sdate3 else [len(gap1), len(gap2)]

# Create DataFrame for gap log
gaplog = pd.DataFrame({
    'site_name': site_name,
    'startdates': startdates,
    'enddates': enddates,
    'missing_observations': missing_observations
})

# Create output directory
full_path = os.path.join(os.getcwd(), f"{site_name}_{deploy}")
os.makedirs(full_path, exist_ok=True)
gapfname = f"{site_name}_{deploy}_Gap_WS_DataLog.csv"
gaplog.to_csv(os.path.join(full_path, gapfname), index=False, quoting=1)

# Combine real data from HOBO loggers with dummy gap data
data = pd.concat([data, gapdata], ignore_index=True)

# Sort combined data by numeric date/time field
data.sort_values(by='sort', inplace=True)

# Create a sequence of numbers for each data record
data['#'] = np.arange(1, len(data) + 1)

# Reduce dataset to necessary fields
data = data[["#", f"Date-Time ({tzhobo})", "Ch:1 - WindSpd - Speed  (m_s)", "Ch:1 - WindSpd - SpeedMax : Max (m_s)"]]

# Reformat columns to match HOBO output formatting
data['#'] = data['#'].astype(np.int32)
data["Ch:1 - WindSpd - Speed  (m_s)"] = pd.to_numeric(data["Ch:1 - WindSpd - Speed  (m_s)"], errors='coerce')
data["Ch:1 - WindSpd - SpeedMax : Max (m_s)"] = pd.to_numeric(data["Ch:1 - WindSpd - SpeedMax : Max (m_s)"], errors='coerce')

# RENAME COMBINED DATA SET
file = os.path.basename(Files[-1])
sn = file[:8]
date = pd.to_datetime(data[f"Date-Time ({tzhobo})"].iloc[-1])
formatted_date = date.strftime("%Y%m%d%H%M%S")
fname = f"{sn} {formatted_date}.csv"

# Export combined data to CSV
data.to_csv(os.path.join(full_path, fname), index=False, quoting=1)