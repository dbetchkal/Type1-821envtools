import os
import tkinter as tk
from tkinter import filedialog
################ START USER INPUT ##################
# Set site parameters
# Incorrect site
site_from = "your_site_code" # Typically four letter park code and 3 digit numeric code. Sample dataset ex. (CARE010)
# Correct site
site_to = "your_deployment_date" # Typically four letter park code and 3 digit numeric code. Sample dataset ex. (CARE001)

# Specify the file type to change (.txt, .wav, etc.)
filetype = ".txt"  # Extension to look for
######### END USER INPUT ###################################

# Function to choose a directory
def choose_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory()
    return directory

# Navigate to the folder where files need to be changed
path = choose_directory()
print("Selected directory:", path)

# Change the working directory
os.chdir(path)

# List files with the specified extension
files = [f for f in os.listdir(path) if f.endswith(filetype)]

# Change the part that needs to be changed (From: site_from to: site_to)
new_names = [f.replace(site_from, site_to) for f in files]

# Rename all files in the directory
for old_name, new_name in zip(files, new_names):
    os.rename(old_name, new_name)

# Verify the changes
new_files = [f for f in os.listdir(path) if f.endswith(filetype)]

# Print the new file names to verify changes
print("New file names:")
for f in new_files:
    print(f)