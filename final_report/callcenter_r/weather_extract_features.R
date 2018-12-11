# extract features from raw weather warning data
# merge with calls (in order to predict expected calls)
library(lubridate)
library(zoo)
library(xts)
library(stringr)

Sys.setenv(TZ='UTC')


we <- read.csv("weather_raw.csv",stringsAsFactors = FALSE)
we$date<-as.Date(we$date,"%b %d, %Y")
codes<-str_split_fixed(we$code, "-", 4)
we$severity<-codes[,1]
we$tornado<-substring(codes[,2],2)
we$wind<-substring(codes[,3],2)
we$hail<-substring(codes[,4],2)
we$state_count<-as.data.frame(unlist(lapply(we$states,function(x) length(unlist(strsplit(x,","))))))[,1]
we$nj<-as.data.frame(grepl("NJ",we$states))[,1]
we$pa<-as.data.frame(grepl("PA",we$states))[,1]
we$year<-as.data.frame(format(we$date,"%Y"))[,1]
we$month<-as.data.frame(format(we$date,"%m"))[,1]
we$day<-as.data.frame(format(we$date,"%d"))[,1]

#write.csv(we,"weather.csv",row.names = FALSE)

#join data
dt <- read.csv("tz.csv",stringsAsFactors = FALSE)
t<-ymd_hms(dt$timeStamp)
ts <- xts(rep.int(1,length(t)),as.POSIXct(t))
daily<-apply.daily(ts,sum)
daily[c(head(we$date))]
we$calls<-as.data.frame(unlist(sapply(we$date,function(x) daily[as.character(x)])))[,1]
View(we)
#remove old textual columns
we$date<-NULL
we$code<-NULL
we$states<-NULL
we$severity<-as.data.frame(unlist(sapply(we$severity, switch, "ENH" = 4, "HIGH" = 6, "MDT" = 5, 
                                         "MRGL" = 2, "SLGT" = 3, "TSTM" = 1, USE.NAMES = F)))[,1]

write.csv(we,"weather_calls.csv",row.names = FALSE)
