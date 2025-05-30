rm(list=ls())

################ START USER INPUT ##################
# Enter site name
sitename <- "your_site_code" # Typically four letter park code and 3 digit numeric code. Sample dataset ex. (CARE004)
# Enter deployment start date
deploy <- "your_deployment_date" # Typically 8 digits representing the day of deployment in YYYYMMDD. Sample dataset ex. (20241009)
# Enter hours to change clock forward or backward
hrs <- 1
# Enter direct, + or -
direction <- "+"

######### END USER INPUT ###################################





packages = c("EnvStats", "reshape2",
             "ggplot2", "ggthemes",
             "pander", "dplyr",
             "lubridate", "readxl","tcltk",
             "svDialogs","tcltk2", "tidyverse","vtable",
             "data.table","ggpubr","knitr","readr",
             "sjmisc","janitor","plyr","writexl", "svDialogs")

## Now load or install & load all
package.check <- lapply(
  packages,
  FUN = function(x) {
    if (!require(x, character.only = TRUE)) {
      install.packages(x, dependencies = TRUE)
      library(x, character.only = TRUE)
    }
  }
)


##Navigate to the SLM files needing time change
#notadjusted
Files <- choose.files()
#create dataframe
data<-read_delim(file=Files, delim = ",",col_names=TRUE)
#  hours to change. Input the number of hours to change
hrs <- hours(hrs) 

#Change the operator in the following folder to + or - depending on the time change direction
# getting current time field and pasting over it by adding or subtracting the hour
data$`              Date/Time              ` <- do.call(direction,list(as_datetime(data$`              Date/Time              `), hrs)) 
# ensure that the hour is formatted with single digit (without the zero in single digit hours)
data$`              Date/Time              ` <- gsub("(^[0-9]{4}-[0-9]{2}-[0-9]{2}) (0?)([0-9]{1}):", "\\1 \\3:", 
                                                           format(data$`              Date/Time              `, "%Y-%m-%d %H:%M:%S"))




# Add space after the 10th character in the date/time field
data$`              Date/Time              ` <- paste0(substr(data$`              Date/Time              `, 1, 10), " ", 
                   substr(data$`              Date/Time              `, 11, 
                          nchar(data$`              Date/Time              `)))



# Store the first date/time value
oldvalue <- data[1, 2]
print(oldvalue)  # Print for verification

# Determine the length of the old date/time string
oldvalue_datelength <- nchar(oldvalue)
print(oldvalue_datelength)

# Get the number of files
file_num <- length(Files)

# Store temporary new value if needed
newvalue <- paste0(substr(oldvalue, 1, 10), "  0:00:00")
nchar(newvalue)  # Print character length to confirm

# Check if the date needs to be changed
datechange <- ifelse(oldvalue_datelength == 20, "Y", "N")



# Update the date if needed
if (datechange == "Y") {
  data[1, 2] <- newvalue
}

#get original file name
file=basename(Files)

full_path <- file.path(getwd(), paste0(sitename,"_",deploy))

dir.create(full_path, recursive = TRUE)



# Write the data to a CSV file
write.csv(data, file.path(full_path, file), row.names = FALSE, quote = FALSE)








