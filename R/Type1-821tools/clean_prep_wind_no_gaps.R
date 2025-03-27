# Clear the workspace
rm(list = ls())

########################### START USER INPUT ###########################
# Enter site name
site_name <- "CARE001"
# Enter deployment start date
deploy <- "20241008"

############################# END USER INPUT ##########################

# List of required packages
packages <- c(
  "EnvStats", "reshape2", "ggplot2", "ggthemes",
  "pander", "dplyr", "lubridate", "readxl",
  "tcltk", "svDialogs", "tcltk2", "tidyverse",
  "vtable", "data.table", "ggpubr", "knitr",
  "readr", "sjmisc", "janitor", "plyr",
  "writexl"
)

# Function to load or install required packages
lapply(packages, function(pkg) {
  if (!require(pkg, character.only = TRUE)) {
    install.packages(pkg, dependencies = TRUE)
    library(pkg, character.only = TRUE)
  }
})

############## START PROCESS #############################


# Choose files; only .csv from all HOBO exports for a given site/deployment
# Ensure the date/time format is: '%m/%d/%Y %H:%M:%S'
files <- choose.files()
# Read the files, assuming comma separator
data <- as.data.frame(read_delim(file = files, delim = ",", col_select = c(1:4), col_names = FALSE, skip = 1))
# extract time zone
tzhobo <- substr(gsub(".*\\((.*)\\).*", "\\1", basename(files)), 6,8)


# Rename column 
names(data)[1] <- "#"
names(data)[2] <- paste0("Date-Time (",tzhobo,")")
names(data)[3] <- "Ch:1 - WindSpd - Speed  (m_s)"
names(data)[4] <- "Ch:1 - WindSpd - SpeedMax : Max (m_s)"
# RENAME COMBINED DATA SET
# Must be in the following format: 
# NEW: SERIALNUMBER YYYY-DD-MM HHmmss.csv 
# Using the last date of the SLM sample or the last download date of the HOBO
tzhobo <- substr(gsub(".*\\((.*)\\).*", "\\1", basename(files)), 6,8)
file_name <- basename(tail(files, n = 1))
serial_number <- substr(file_name, 1, 8)
date <- tail(data[2], n = 1)
date <- mdy_hms(date)
formatted_date <- gsub(":", "", as.character(date))  # Remove colons for the filename
fname <- paste(serial_number," ", formatted_date, ".csv", sep = "")

# Create full path for the output directory
full_path <- file.path(getwd(), paste0(site_name, "_", deploy))
dir.create(full_path, recursive = TRUE)

# Export combined data to CSV; will be placed in the specified project folder
write.csv(data, file.path(full_path, fname), row.names = FALSE, quote = FALSE)

# Print confirmation message about the exported file
cat("Data has been exported to:", file.path(full_path, fname), "\n")
