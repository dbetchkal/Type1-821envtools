import os
import pandas as pd
from datetime import datetime, timedelta
from tkinter import filedialog
import tkinter as tk
import numpy as np
import re

# Clear the workspace (not applicable in Python)

# ################ START USER INPUT ##################
# Enter site name for file prefix
sitename = "CARE004"
# Enter deployment start date
deploy = "20241009"
# Enter hours to change clock forward or backward
hrs = 1
# Enter direction forward "+" or backward "-"
direction = "+"

# ######### END USER INPUT ###################################

# Function to select files
def select_files():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    files = filedialog.askopenfilenames(title="Select Files",
                                         filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    return files

# Load the files needing time change
Files = select_files()

# Create dataframe
data = pd.concat((pd.read_csv(file) for file in Files), ignore_index=True)

# Change the operator based on the direction
if direction == "+":
    delta = timedelta(hours=hrs)
else:
    delta = timedelta(hours=-hrs)

# Change Date/Time column
data['              Date/Time              '] = pd.to_datetime(data['              Date/Time              '])
data['              Date/Time              '] += delta

# Format the Date/Time column manually to get the desired format
data['              Date/Time              '] = data['              Date/Time              '].dt.strftime('%Y-%m-%d %H:%M:%S')
data['              Date/Time              '] = data['              Date/Time              '].str.replace(r'(^[0-9]{4}-[0-9]{2}-[0-9]{2}) (0?)([0-9]{1}):', r'\1 \3:', regex=True)

# Add space after the 10th character
data['              Date/Time              '] = data['              Date/Time              '].apply(
    lambda x: f"{x[:10]} {x[10:]}"
)

# Store the first date/time value
oldvalue = data.iloc[0, 1]
print(oldvalue)  # Print for verification

# Determine the length of the old date/time string
oldvalue_datelength = len(oldvalue)
print(oldvalue_datelength)

# Get the number of files
file_num = len(Files)

# Store a temporary new value if needed
newvalue = f"{oldvalue[:10]} 00:00:00"
print(len(newvalue))  # Print character length to confirm

# Check if the date needs to be changed
datechange = "Y" if oldvalue_datelength == 20 else "N"

# Update the date if needed
if datechange == "Y":
    data.iloc[0, 1] = newvalue

# Get original file name
file = os.path.basename(Files[0])

# Create output directory
full_path = os.path.join(os.getcwd(), f"{sitename}_{deploy}")
os.makedirs(full_path, exist_ok=True)

# Write the data to a CSV file
output_file = os.path.join(full_path, file)
data.to_csv(output_file, index=False, quoting=False)

print(f"Data saved to {output_file}")