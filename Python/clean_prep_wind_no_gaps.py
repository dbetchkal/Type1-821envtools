import os
import pandas as pd
from tkinter import filedialog, Tk
from datetime import datetime
import numpy as np

# Clear the workspace equivalent (in Python, we usually just reset variables)

# Initialize Tkinter and hide the root window
root = Tk()
root.withdraw()  # Hide the root window

########################### START USER INPUT ###########################
# Enter site name
site_name = "CARE001"
# Enter deployment start date
deploy = "20241008"
############################# END USER INPUT ##########################

# List of required packages
packages = [
    "pandas", "numpy"
]

# Check and install required packages
for pkg in packages:
    try:
        __import__(pkg)
    except ImportError:
        os.system(f"pip install {pkg}")

############## START PROCESS #############################

# Import template dataset to match headings for incoming datasets
template = pd.read_csv("headingtemplate.csv", usecols=[0, 1, 2, 3])
# Remove all data from the template (keeping only the header)
template = template.iloc[0:0]  # Empty DataFrame with the same columns as template

# Choose files; only .csv from all HOBO exports for a given site/deployment
# Ensure the date/time format is: '%m/%d/%Y %H:%M:%S'
files = filedialog.askopenfilenames(title="Select HOBO CSV files", filetypes=[("CSV files", "*.csv")])

# Read the files with a comma separator
data_frames = [pd.read_csv(file, usecols=[0, 1, 2, 3], skiprows=1) for file in files]
data = pd.concat(data_frames, ignore_index=True)

# Replace column headings with those from template
data.columns = template.columns

# RENAME COMBINED DATA SET
# Format: NEW: SERIALNUMBER YYYYDDMMHHmmss.csv
file_name = os.path.basename(files[-1])  # Get the last file's name
serial_number = file_name[:8]  # Extract the serial number

# Retrieve last date
date = data['Date-Time (PDT)'].iloc[-1]  # Assuming the column name is 'Date-Time (PDT)'
date = pd.to_datetime(date, format='%m/%d/%Y %H:%M:%S')

# Remove colons for the filename
formatted_date = date.strftime('%Y%m%d %H%M%S').replace(":", "")
fname = f"{serial_number} {formatted_date}.csv"

# Create full path for the output directory
full_path = os.path.join(os.getcwd(), f"{site_name}_{deploy}")
os.makedirs(full_path, exist_ok=True)

# Export combined data to CSV in the specified project folder
data.to_csv(os.path.join(full_path, fname), index=False, quoting=1)

# Print confirmation message about the exported file
print(f"Data has been exported to: {os.path.join(full_path, fname)}")