# arima hours
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

h<-period.apply(ts, endpoints(ts, "hours"), sum)
head(h)

model<-arima(h,order=c(1,0,1),seasonal=list(order=c(1,0,1),period=24*7))
model
describe(residuals(model))
plot(fitted(model))
str(model)

plot(coredata(h)[1:100],type="l")
lines(fitted(model)[450:550],col="red")
plot(fitted(model)[100:200],col="red" )
fit<-fitted(model)
?arima.xts
x<-predict(model,n.ahead = 96)
up<-x$pred+2*x$se
down<-x$pred-2*x$se
plot(x$pred,ylim=c(min(down),max(up)))
lines(up,col="red")
lines(down,col="red")

train_d<-h["2015-12-14/2017-05-20"]
test_d<-h["2017-05-20 00:00:00/2017-06-04 00:00:00"]
train_m<-arima(train_d,order=c(1,0,1),seasonal=list(order=c(1,0,1),period=24*7))

pred<-predict(train_m,n.ahead= 96)
t<-test_d[1:96]
up<-pred$pred+2*pred$se
down<-pred$pred-2*pred$se
lim<-c(min(down),max(up))
dev.off()
plot(t,ylim=lim)
lines(t,col="yellow",lwd=4)
lines(index(t),coredata(pred$pred),col="red")
lines(index(t),coredata(down),col="blue")
lines(indraiex(t),coredata(up),col="orange")
plot(index(t),coredata(up),type="l")
plot(index(t),coredata(down),type="l",ylim=lim)

small<-h["2016-06-14/2016-09-20"]
plot(diff(small,7))
plot(diff(small,7*24))
plot(diff(small,24))
plot(diff(diff(small,24),1))
plot(diff(diff(small,7*24),1))
plot(diff(diff(small,7*24),7*24))
lines(diff(small,7*24),col="red")
lines(diff(diff(small,7*24),7*24),col="red")
acf(diff(small,7*24))
acf(small)

Box.test(resid(train_m),lag=7*24,type="Ljung",fitdf = 2)

