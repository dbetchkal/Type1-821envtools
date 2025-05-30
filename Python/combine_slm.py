import os
import pandas as pd
from datetime import datetime
from tkinter import filedialog, Tk
import numpy as np

# Clear the workspace (in Python, we usually just reset variables)
# Tkinter is used to create a file selection dialog
root = Tk()
root.withdraw()  # Hide the root window

################ START USER INPUT ##################
# Enter site name for file prefix
sitename = "your_site_code" # Typically four letter park code and 3 digit numeric code. Sample dataset ex. (YOSE013)
# Enter deployment start date
deploy = "your_deployment_date" # Typically 8 digits representing the day of deployment in YYYYMMDD. Sample dataset ex. (20240618)

######### END USER INPUT ###################################

# Assuming the deployment produces files with specific suffixes
files = filedialog.askopenfilenames(title="Select SLN Files", filetypes=[("CSV files", "*.csv")])

# Read the files into a list, assuming comma separator
spl_files_df = [pd.read_csv(file) for file in files]

# Bind the data together into one DataFrame
data = pd.concat(spl_files_df, ignore_index=True)

# Store the first date/time value
oldvalue = data.iloc[0, 1]
print(oldvalue)  # Print for verification

# Determine the length of the old date/time string
oldvalue_datelength = len(oldvalue)
print(oldvalue_datelength)

# Get the number of files
file_num = len(files)

# Store temporary new value if needed
newvalue = f"{oldvalue[:10]}  0:00:00"

# Check if the date needs to be changed
datechange = "Y" if oldvalue_datelength == 20 else "N"

# Extract basename from the last file
fname = os.path.basename(files[file_num - 1])

# Update the date if needed
if datechange == "Y":
    data.iloc[0, 1] = newvalue

# Construct the full path
full_path = os.path.join(os.getcwd(), f"{sitename}_{deploy}")

# Create the directory if it doesn't exist
os.makedirs(full_path, exist_ok=True)

# Create the final file path name
fullname = f"{sitename}_{fname}"

# Write the data to a CSV file
data.to_csv(os.path.join(full_path, fullname), index=False, quoting=1)

print(f"Data has been written to: {os.path.join(full_path, fullname)}")