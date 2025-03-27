rm(list=ls())
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
dlfile <- choose.files()
#create dataframe
dldata<-read_delim(file=dlfile, delim = ",",col_names=TRUE)


##Navigate to the SLM files needing time change
Files <- choose.files()
#create dataframe
data<-read_delim(file=Files, delim = ",",col_names=TRUE)
#  hours to change. Input the number of hours to change
hrs <- hours(0) 

#Change the operator in the following folder to + or - depending on the time change direction
# getting current time field and pasting over it by adding or subracting the hour
data$`              Date/Time              ` <- as_datetime(data$`              Date/Time              `) + hrs #change operator to add/subract
data$`              Date/Time              ` <- as.character.Date(data$`              Date/Time              `)
#get original file name
file=basename(Files)

#Export csv. Will be placed into the R Project folder and can be moved to the 
#SPL folder
write.csv(data, file,row.names=FALSE)
?write.csv()
