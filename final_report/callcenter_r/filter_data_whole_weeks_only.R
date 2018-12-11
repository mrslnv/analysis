## This script filters data - subsetting to the whole weeks
## result (2015-12-14/2017-06-04) is in file "time.csv"
# reads "tz.csv"

library(lubridate)
library(zoo)
library(xts)
library(psych)
library(forecast)
library(xtsExtra)

#ignore timezones (avoid the danger of using CET and struggle with daylight changes)
Sys.setenv(TZ='UTC')


dt <- read.csv("tz.csv",stringsAsFactors = FALSE)

#Create time series to analyze call frequency (XTS objects)
t<-ymd_hms(dt$timeStamp)
ts <- xts(rep.int(1,length(t)),as.POSIXct(t))

daily <- apply.daily(ts,sum)
describe(daily)

#cut off data to whole weeks
#14.12 - Mon (1680 before = 0.6%)
plot(daily["2015-12-10/2015-12-16"])

cut_off<-sum(daily["2015-12-10/2015-12-13"])/sum(daily)
paste(c("Cutting off ",cut_off*100," %"), collapse = "")
#5.6. - Mon (925 after = 0.4%)
plot(daily["2017-05-30/2017-06-07"])
cut_off<-sum(daily["2017-06-05/2017-06-10"])/sum(daily)
paste(c("Cutting off ",cut_off*100," %"), collapse = "")

#Filter data! Analyze <14.12. 2015 (Mon) - 5.6. 2017) (Mon)
ts<-ts["2015-12-14/2017-06-04"]
write.csv(list("Time of calls"=index(ts)),"time.csv",row.names = FALSE)

paste("Data subset(2015-12-14/2017-06-04) written to time.csv")
