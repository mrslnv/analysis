## This script assumes that data was filters (see filter_data_whole_weeks_only.R )
# reads "time.csv"

library(lubridate)
library(zoo)
library(xts)
library(psych)
library(forecast)
library(xtsExtra)

#ignore timezones (avoid the danger of using CET and struggle with daylight changes)
Sys.setenv(TZ='UTC')

dt <- read.csv("time.csv",stringsAsFactors = FALSE)

#Create time series to analyze call frequency (XTS objects)
t<-ymd_hms(dt$Time.of.calls)
ts <- xts(rep.int(1,length(t)),as.POSIXct(t))

daily <- apply.daily(ts,sum)
describe(daily)

#Overall trend of daily rate
plot.xts(daily,major.ticks="months",major.format="%b", las=2,type="l",lwd=4,
         main="Daily calls (irregular peaks)")

#Prepare hour rates per days of week
h<-period.apply(ts, endpoints(ts, "hours"), sum)
#split by day of week
dow<-split.default(h, format(index(h), "%a"))
#compute avg for every hour of each day of week
dowAgg <- lapply(dow,function(x) aggregate(x, format(index(x), "%H"), mean))  
dowSum <- do.call(merge, dowAgg)[,c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat","Sun")]

plot(dowSum, type="l", nc=1, ylim=range(dowSum), main="Average hourly calls", 
     las=1,col = c(rep("blue",5),rep("navy",2)))
boxplot(coredata(dowSum),ylab="Num. of calls per hour",col="gray",at=c(1,2,3,4,5,7,8),
        yaxt="n", main="Call distribution by day of week")
axis(2, at = seq(4, 30, by = 1), las=2)

# looking into some peaks - around christmas and new year
plot.xts(daily["2015-12-11/2016-01-20"],major.ticks="days",major.format="%d")
plot.xts(daily["2016-12-11/2017-01-20"],major.ticks="days",major.format="%d")

#analysis
#acf spikes every 7 days, also alot from the previous day
dacf<-acf(daily,plot=FALSE)
#:-) it works for xts directly! xtsEstra! acf(ts(coredata(daily),7))
plot(dacf,xaxt="n",main="ACF for #calls daily")
axis(1, at = seq(0, 28, by = 1), las=2)

#fitting seasonal ARIMA
model<-arima(daily,order=c(1,0,1),seasonal=list(order=c(1,0,1),period=7))
model
describe(residuals(model))
plot(residuals(model))


#hourly? 
#todo


#for a sub set
plot(coredata(daily)[200:300],type="l",ylab="Num. of calls per day",xlab="Series of 100 days (from 30 Jun)",main = "Real vs. predicted data(Seasonal ARIMA)")
lines(fitted(model)[200:300],col="red")

#for a sub set
plot(coredata(daily)[400:500],type="l")
lines(fitted(model)[400:500],col="red")

#for a sub set
plot(coredata(daily)[450:550],type="l")
lines(fitted(model)[450:550],col="red")


#check fit with Poisson Mondays 13-14
d<-h[which(.indexhour(h)==13 & .indexwday(h)==1)]
describe(d)
plot(coredata(d),type = "l")
spois<-rpois(577,mean(d))
qqplot(spois,coredata(d),main="QQ plot - Pois(22.75) vs. Mondays 13-14)", xlab = "",ylab = "")
abline(0,1)

#for longer period, there is NO FIT!
qqplot(spois,coredata(dow[2]$Mon["T09:00/T18:00"]),main="QQ plot - Pois(22.75) vs. Mondays 9-18)", xlab = "",ylab = "")
abline(0,1)

