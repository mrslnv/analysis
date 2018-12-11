#install.packages("zoo")
require("zoo")
#install.packages("dplyr")
require("dplyr")

#install.packages("stringr")
require("stringr")

#install.packages("plot3D")
require("plot3D")

#read.zoo(file="w:\\Code\\GoodAI\\short.csv", sep = ",", header = TRUE, index = "timeStamp",
#            format = "%Y-%m-%d %H:%M:%S", tz = "GMT")

dt <- read.csv("w:\\Code\\GoodAI\\tz.csv",stringsAsFactors = FALSE)

t<-as.POSIXct(dt$timeStamp)
ts <- xts(rep.int(1,length(t)),as.POSIXct(t))
daily <- apply.daily(ts,sum)
describe(daily)
plot.xts(daily,major.ticks="weeks",major.format="%W")

em<-dt %>%  filter(str_detect(title, 'EMS'))
dt <- NULL
outliers <- em[em$lng<(-75.79),]

# only 3 records are outside NY/PHI region
#View(outliers)

em <- em[em$lng>(-75.79),]

summary(em$lng)
summary(em$lat)

x_c <- cut(em$lng, 29)
y_c <- cut(em$lat, 29)
z <- table(x_c, y_c)
#hist3D(z=z, border="black")
image2D(z=z,border="black")

em$desc <- NULL
em$zip <- NULL
em$title <- NULL
em$twp <- NULL
em$e <- NULL

Sys.setenv(TZ='UTC')

emt <- em
emt$time <- strptime(em$timeStamp,format="%Y-%m-%d %H:%M:%S",tz="UTC")
em$timeStamp <- NULL



write.csv(em,"emergency-clean.csv")

em<- NULL

emt$lat <- NULL
emt$lng <- NULL
emt$timeStamp <- NULL

#14.12 - Mon (622 before)
lTime<-strptime("2015-12-14",format="%Y-%m-%d",tz="UTC")
#5.6. - Mon (467 after)
hTime<-strptime("2017-06-05",format="%Y-%m-%d",tz="UTC")
#filtered time
ft <- emt[emt$time >= lTime & emt$time <= hTime,]

write.csv(ft,"time.csv")

#install.packages("tseries")
require("tseries")
#install.packages("xts")
require("xts")
#install.packages("quantmod")
#require("quantmod")
require("psych")


ts <- xts(rep.int(1,length(ft)),as.POSIXct(ft,tz="UTC"))

daily <- apply.daily(ts,sum)
describe(daily)
plot.xts(daily,major.ticks="weeks",major.format="%W")

weekly <- apply.weekly(ts,sum)
describe(weekly)
plot.xts(weekly,major.ticks="weeks",major.format="%W")

monthly <- apply.monthly(ts,sum)
describe(monthly)
plot.xts(monthly,major.ticks="months",major.format="%b")

#dec21ts<-ts["2015-12-21"]
#hist(dec21ts,"hours")
#dec21byHour<-period.apply(dec21ts, endpoints(dec21ts, "hours"), sum)
#plot(period.apply(dec21ts, endpoints(dec21ts, "hours"), sum))

#b<-ts["T10:00/T21:00"]
#View(b)

h<-period.apply(ts, endpoints(ts, "hours"), sum)
dow<-split.default(h, format(index(h), "%A"))

dowAgg <- lapply(dow,function(x) aggregate(x, format(index(x), "%H"), mean))  
dowSum <- do.call(merge, dowAgg)[,c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday")]
#index(dowSum) <- as.POSIXct(index(dowSum), format="%HH")
plot(dowSum, type="l", nc=1, ylim=range(dowSum), main="Average daily calls", las=1)

dowStd <- lapply(dow,function(x) aggregate(x, format(index(x), "%H"), sd))  
dowStdSum <- do.call(merge, dowStd)[,c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday")]
index(dowStdSum) <- as.POSIXct(index(dowStdSum), format="%HH")
plot(dowStdSum, type="l", nc=1, ylim=range(dowStdSum), main="Std daily", las=1)
View(dowStdSum)

#peek into Mon 9-10
hist(dow[2]$Monday["T09:00/T10:00"],11)
describe(dow[2]$Monday["T09:00/T10:00"])
#8-11 - pretty normal dist
hist(dow[2]$Monday["T08:00/T11:00"],11)
# poisson? mean = sd^2 --> but hist is normal => X-lambda is NORMAL
describe(dow[2]$Monday["T11:00/T17:00"])
hist(dow[2]$Monday["T11:00/T17:00"])

#mon<-h[.indexwday(h)==1]
#e<-endpoints(b, "hours")
#c<-period.apply(ts, endpoints(ts, "hours"), sum)
#plot(c)
#hist(c)
#summary(c)

dt <- read.csv("q2-output.csv",stringsAsFactors = FALSE)
#emt$time <- strptime(em$timeStamp,format="%Y-%m-%d %H:%M:%S",tz="UTC")
str(dt)
hist(dt$queue,13)
l<-dt[dt$queue>1,]
hist(l$queue,13)
ll<-dt[dt$queue>2,]
hist(ll$queue,13)
lll<-dt[dt$queue>3,]
describe(dt$queue)

l$ntime <- strptime(l$time,format="%Y-%m-%d %H:%M:%S",tz="UTC")
l.xts<-xts(l$queue,as.POSIXct(l$ntime,tz="UTC"))
#l.xts<-l.xts["T00:00/T06:00"]
hh<-period.apply(l.xts, endpoints(l.xts, "hours"), mean)

dowl<-split.default(hh, format(index(hh), "%A"))

dowAggl <- lapply(dowl,function(x) aggregate(x, format(index(x), "%H"), mean))  
dowSuml <- do.call(merge, dowAggl)[,c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday")]
#index(dowSum) <- as.POSIXct(index(dowSum), format="%HH")
plot(dowSuml, type="l", nc=1, ylim=range(dowSuml), main="Average daily calls", las=1)

describe(dowl[2]$Monday["T05:00/T06:00"])
hist(dowl[2]$Monday["T09:00/T18:00"])


#time series data
library(foreign)
bjg<-read.dta("c:\\Temp\\air2.dta")
airline.ts <- ts(bjg[, 1], start=c(1949,1), freq=12)
bjg[, 1]
airline.ts <- ts(bjg[, 1], start=c(1949,1), freq=12)
head(time(airline.ts))
time(airline.ts)[]

myDates = seq(as.Date("2003-11-19"), as.Date("2003-12-30"),by="2 days") 

daily <- apply.daily(ts,sum)
describe(daily)
plot.xts(daily,major.ticks="weeks",major.format="%W")

#filter using index
x <- timeBasedSeq('2010-01-01/2010-01-02 12:00')
x <- xts(1:length(x), x)
# all obs. in the first 6 and last 3 minutes of the
# 8th and 15th hours on each day
x[.indexhour(x) %in% c(8,15) & .indexmin(x) %in% c(0:5,57:59)]
