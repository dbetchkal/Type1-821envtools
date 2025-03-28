# Instructions for Data Processing
#### NSNSD Users: Download 'SampleData' from sharepoint software and scripts location to run through each process
## 1. Download LD SPL Data

### Steps to Download:
- Open G4 LD Utility software.<br>
- Connect LD 821 to your computer using a micro USB.<br>
- In the left margin of G4 Utility, select your LD 821 (identified by SN or user-specified name).<br>
- In the main window, select![image](https://github.com/user-attachments/assets/a33079b2-b72e-404a-a08b-c92e8bb3b246) <br>
- Select  the most recent file![image](https://github.com/user-attachments/assets/122995bd-b741-4ebf-9528-68912d440fb4) <br>
 and download ![image](https://github.com/user-attachments/assets/3ad9c0a5-7347-4070-a8cc-f8db4508f421) <br>
- Once downloaded, double-click the file to open it as a tab in the main window.![image](https://github.com/user-attachments/assets/86c6be4d-e0f0-4abe-a53e-62415b9b67b7) <br>
- Select `File > Export to csv`. A window will appear to show where it is saved.![image](https://github.com/user-attachments/assets/9bd4753f-ff86-45ba-b10f-a14ae58b5467) <br>
- Navigate to this location and move the file with the `_Time History.csv` suffix to your SPL folder created in step 1.<br>

### TEMP FIX for AMT ISSUE:
- If you deployed at an hour with two digits (e.g., 10, 11, 12), replace the recorded hour with `0:00:00` at the very first time step.<br>


![image](https://github.com/user-attachments/assets/78a2febf-2687-48d3-b1ec-14f9e69811f0)<br>


### Combine SPL Time History Files:
- Use `Type1-821envtools` in either R or Python:<br>
  - Choose the `combine_slm` script.<br>
  - Enter user input (Site Name and Deployment).<br>
  - Run the script and follow the prompt to select time history files.<br>
  - The script will adjust the first time step if necessary, combine all files, and save the resulting file in the deployment folder of the `Type1-821envtools` project.<br>

## 2. Download the MET Data

### Steps to Download:
- Use the iOS app HoboConnect to download data from the unit.<br>
- In the data tab, click “Export and Share” and then click Done.<br>
- Open the Files app on your phone, browse, and using the three-dot icon, select files to open them in OneDrive (or email them to yourself).<br>

### Clean Data Preparation:
- If your deployment resulted in one continuous file:<br>
  - Use `Type1-821envtools` in either R or Python:<br>
    - Choose the `clean_prep_wind_no_gaps` script.<br>
    - Enter user input (Site Name and Deployment).<br>
    - When prompted, navigate to the exported HOBO output file.<br>
    - Run the script; it will ensure proper headings and file naming for AMT processing.<br>

- If there are data gaps:<br>
  - Note the data gaps and use the `combine_clean_fillgaps_win` script in either R or Python.<br>
  - Enter relevant user input. Specify data gaps as instructed.<br>
  - This script accommodates up to 3 data gaps.<br>
  - Run the script and navigate to existing exported HOBO files when prompted.<br>
  - A cleaned wind file will be outputted with null values in gaps, along with a log of missing data.<br>

### Important Note:
- Always open wind data in Notepad; if opened in Excel, it may reformat the time and drop seconds, causing merge issues with SPL files.<br>

## 3. File Structure for Processing Cleaned Files

- In your deployment folder, create:<br>
  - A `MET` folder.<br>
  - An `SPL` folder, and inside it, create another folder named `NVSPL`. <br>
  ![image](https://github.com/user-attachments/assets/d65f7c13-ceb8-4c85-80f4-a7909361f08a) <br>


## 4. Create NVSPL Files in AMT

- Open AMT v1.8847 and the SPL2NV tool.<br>
- Ensure “Search for wind speed” is checked in options.<br>
- Select `File > Choose SPL Files` and select the SPL file in your project folder.<br>
- Set the Output directory to the NVSPL folder nested within your SPL folder.<br>
- Click “Convert Files.”<br>
- The NVSPL files with merged SPL and MET data should now appear in the NVSPL folder.<br>

Make sure to follow these steps carefully to ensure proper data processing and management.<br>

### Public domain

This project is in the worldwide [public domain](LICENSE.md):

> This project is in the public domain within the United States,
> and copyright and related rights in the work worldwide are waived through the
> [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication.
> By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
