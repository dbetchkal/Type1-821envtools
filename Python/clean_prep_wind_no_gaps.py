import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

# Functionality Description:
# This script processes wind speed data from CSV files exported from HOBO loggers.
# It handles user inputs, file management, and renaming exports based on specific formats.

# Clear the workspace (not necessary in Python but included for clarity)
# This will be done automatically when the script ends.

########################### START USER INPUT ###########################
# Enter site name
site_name = "CARE003"
# Enter deployment start date
deploy = "20241009"
############################# END USER INPUT ##########################

# List of required packages (ensure you have these installed)
required_packages = [
    'pandas',
    'tkinter',  # Included in standard library
]

# Function to prompt for the package installation
def load_packages(packages):
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing package: {package}")
            import pip
            pip.main(['install', package])

load_packages(required_packages)

############## START PROCESS #############################

# Initialize the Tkinter root
root = tk.Tk()
root.withdraw()  # Hide the root window

# Choose files; only .csv from all HOBO exports for a given site/deployment
files = filedialog.askopenfilenames(title="Choose HOBO CSV files", filetypes=[("CSV Files", "*.csv")])

# Read the files, assuming comma as the separator
data_frames = []
for file in files:
    df = pd.read_csv(file, usecols=[0, 1, 2, 3], skiprows=1, header=None)
    data_frames.append(df)

# Concatenate all data into a single DataFrame
data = pd.concat(data_frames, ignore_index=True)

# Extract time zone from the file name
tzhobo = os.path.basename(files[0]).split('(')[-1].split(')')[0][5:8]  # Extract time zone

# Rename column headings
data.columns = [
    "#",
    f"Date-Time ({tzhobo})",
    "Ch:1 - WindSpd - Speed  (m_s)",
    "Ch:1 - WindSpd - SpeedMax : Max (m_s)"
]

# Extract serial number from the last file name
file_name = os.path.basename(files[-1])
serial_number = file_name[:8]

# Extract the last date from the DataFrame for file naming
last_date = data.iloc[-1, 1]  # Assuming the date is in the second column
date = datetime.strptime(last_date, '%m/%d/%Y %H:%M:%S')
formatted_date = date.strftime('%Y%m%d%H%M%S')  # Format date as 'YYYYMMDDHHMMSS'
fname = f"{serial_number} {formatted_date}.csv"

# Create full path for the output directory
full_path = os.path.join(os.getcwd(), f"{site_name}_{deploy}")
os.makedirs(full_path, exist_ok=True)  # Create directory if it doesn't exist

# Export combined data to CSV; will be placed in the specified project folder
data.to_csv(os.path.join(full_path, fname), index=False, header=True)

# Print confirmation message about the exported file
print(f"Data has been exported to: {os.path.join(full_path, fname)}")