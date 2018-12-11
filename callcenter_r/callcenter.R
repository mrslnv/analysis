#library(dplyr)

#library(stringr)

#library(tseries)

#library(tsdecomp)
#library(tsoutliers)

library(zoo)
library(lubridate)
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

plot.xts(daily,major.ticks="months",major.format="%b", las=2,type="l",lwd=4,
         main="Daily calls (irregular peaks)")

#14.12 - Mon (1680 before = 0.6%)
plot(daily["2015-12-10/2015-12-16"])

sum(daily["2015-12-10/2015-12-13"])/sum(daily)

#5.6. - Mon (925 after = 0.4%)
plot(daily["2017-05-30/2017-06-07"])
sum(daily["2017-06-05/2017-06-10"])/sum(daily)

#analyze <14.12. 2015 (Mon) - 5.6. 2017) (Mon)
ts<-ts["2015-12-14/2017-06-04"]
write.csv(list("Time of calls"=index(ts)),"time.csv",row.names = FALSE)
daily <- apply.daily(ts,sum)

#by week days
h<-period.apply(ts, endpoints(ts, "hours"), sum)
dow<-split.default(h, format(index(h), "%a"))

dowAgg <- lapply(dow,function(x) aggregate(x, format(index(x), "%H"), mean))  
dowSum <- do.call(merge, dowAgg)[,c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat","Sun")]
#index(dowSum) <- as.POSIXct(index(dowSum), format="%HH")
plot(dowSum, type="l", nc=1, ylim=range(dowSum), main="Average hourly calls", 
     las=1,col = c(rep("blue",5),rep("navy",2)))
boxplot(coredata(dowSum),ylab="Num. of calls per hour",col="gray",at=c(1,2,3,4,5,7,8),
        yaxt="n", main="Call distribution by day of week")
axis(2, at = seq(4, 30, by = 1), las=2)

# christmas and new year
plot.xts(daily["2015-12-11/2016-01-20"],major.ticks="days",major.format="%d")
plot.xts(daily["2016-12-11/2017-01-20"],major.ticks="days",major.format="%d")


#min stats
min(dowSum)
str(dowSum)
str(coredata(dowSum))
View(coredata(dowSum))

#analysis
#acf spikes every 7 days, also alot from the previous day
dacf<-acf(daily,plot=FALSE)
#:-) it works for xts directly! xtsEstra! acf(ts(coredata(daily),7))
plot(dacf,xaxt="n",main="ACF for #calls daily")
axis(1, at = seq(0, 28, by = 1), las=2)

#arima model
auto.arima(daily,D=5,max.P = 3, max.Q = 5)
#seasonal arima
model<-arima(daily,order=c(1,0,1))
model<-arima(daily,order=c(1,0,1),seasonal=list(order=c(7,0,0)))
model<-arima(daily,order=c(1,0,1),seasonal=list(order=c(8,0,0)))
model<-arima(daily,order=c(1,0,1),seasonal=list(order=c(5,0,0)))
arima(daily,order=c(1,0,1),seasonal=list(order=c(7,1,0)))
model<-arima(daily,order=c(1,0,1),seasonal=list(order=c(8,1,0)))
model<-arima(daily,order=c(1,0,1),seasonal=list(order=c(14,0,0)))
arima(daily,order=c(1,0,1),seasonal=list(order=c(14,1,0)))
arima(daily,order=c(1,0,1),seasonal=list(order=c(14,1,2)))
arima(daily,order=c(1,0,1),seasonal=list(order=c(21,1,2)))
arima(daily,order=c(1,0,1),seasonal=list(order=c(7,7,7)))
#this is a perfect fit
model<-arima(daily,order=c(1,0,1),seasonal=list(order=c(1,0,1),period=7))
model
describe(residuals(model))
plot(residuals(model))


#hourly? todo



#for a sub set
daily[200]
plot(coredata(daily)[200:300],type="l",ylab="Num. of calls per day",xlab="Series of 100 days (from 30 Jun)",main = "Real vs. predicted data(Seasonal ARIMA)")
lines(fitted(model)[200:300],col="red")

#for a sub set
plot(coredata(daily)[400:500],type="l")
lines(fitted(model)[400:500],col="red")

#for a sub set
plot(coredata(daily)[450:550],type="l")
lines(fitted(model)[450:550],col="red")


#fit with Poisson
hist(dowl[2]$Monday["T09:00/T18:00"])

d<-h[which(.indexhour(h)==13 & .indexwday(h)==1)]
describe(d)
plot(coredata(d),type = "l")
View(d)
spois<-rpois(577,mean(d))
qqplot(spois,coredata(d),main="QQ plot - Pois(22.75) vs. Mondays 9-18)", xlab = "",ylab = "")
abline(0,1)
mean(d)

hist(dow[2]$Mon["T13:00/T14:00"],11)
  plot(dowAgg$Mon,xaxt="n",yaxt="n")
axis(1, at = seq(0, 24, by = 1), las=1)
axis(2, at = seq(5, 30, by = 2), las=2)

#TODO!




#looking into location data a bit
boxplot(dt$lng)
boxplot(dt$lat)
outliers <- dt[dt$lng<(-80) | dt$lat<(38),]

ioutliers <- dt[dt$lng<(-80),]
outliers <- dt[dt$lat<(38),]

f1<-dt[dt$lng>(-80),]
boxplot(f1$lng)


f2<-dt[dt$lat>(38),]
boxplot(f1$lat)



