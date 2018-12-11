
library(lubridate)
#library(graphics)
Sys.setenv(TZ='UTC')


wt <- read.csv("wtime-output-basic.csv",stringsAsFactors = FALSE)
wt <- read.csv("wtime-output.csv",stringsAsFactors = FALSE)
t<-ymd_hms(wt$time)
ts <- xts(wt$delay,as.POSIXct(t))
length(ts[ts>300])
plot(ts[ts>300],major.format="%d %b",las=2,type="p")
mean(wt$delay)

day<-apply.daily(prob,mean)
prob_day <- day[day>900] #days[wait time > 15 min]
plot(prob_day,type="p")
length(prob_day)

wt[wt$delay>900,]

wt[wt$delay>600,]

x<-apply.daily(ts,mean)
length(x)

prob<- ts[ts>120]
length(prob)

day<-apply.daily(prob,mean)

day[day>600] # only 2
hist(day[day<600])
prob_day <- day[day>300] #days[wait time > 15 min]
length(prob_day)
plot(prob_day,type="p")

#2016-02-24 --- here, it is crazy (only this)
ts[ts>2000]


#day sum?
day<-apply.daily(prob,sum)

#hour mean?
h<-period.apply(ts, endpoints(ts, "hours"), mean)
head(h[h>100])

h[h>240]

h<-period.apply(ts, endpoints(ts, "hours"), mean)
plot(h["2016-02-24 15:00:00/2016-02-25 02:00:00"])
dow<-split.default(h, format(index(h), "%a"))

#another extreme: 2016-01-12
plot(h["2016-01-12 18:00:00/2016-01-12 23:59:00"])


dowAgg <- lapply(dow,function(x) aggregate(x, format(index(x), "%H"), mean))  
dowSum <- do.call(merge, dowAgg)[,c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat","Sun")]
#index(dowSum) <- as.POSIXct(index(dowSum), format="%HH")
plot(dowSum, type="l", nc=1, ylim=range(dowSum), main="Average daily calls", 
     las=1,col = c(rep("blue",5),rep("navy",2)))
boxplot(coredata(dowSum),ylab="#Calls in a day",col="gray",at=c(1,2,3,4,5,7,8),
        yaxt="n")
axis(2, at = seq(150, 300, by = 10), las=2)
View(dowAgg[6]$Tue)

plot(dowAgg[6]$Tue,type="p",xaxt="n")
axis(1, at = seq(0, 23, by = 1), las=1)
#10 & 11 Tue is crazy

tue10_11 <-dow[6]$Tue["T09:00/T18:00"]
plot(tue10_11,type="p")
View(tue10_11)

boxplot(coredata(ts[ts>60]))
summary(coredata(prob))
plot(ts[ts>1200])
prob

t<-ymd_hms(dt$timeStamp)
ts <- xts(rep.int(1,length(t)),as.POSIXct(t))
h<-period.apply(ts, endpoints(ts, "hours"), sum)
plot(h["2016-02-24 15:00:00/2016-02-25 02:00:00"])

vehicle<-dt %>%  filter(str_detect(title, 'VEHICLE'))
head(vehicle)
t<-ymd_hms(vehicle$timeStamp)
ts <- xts(rep.int(1,length(t)),as.POSIXct(t))
h<-period.apply(ts, endpoints(ts, "hours"), sum)
plot(h["2016-02-22 15:00:00/2016-02-27 02:00:00"])


vehicle<-dt %>%  filter(str_detect(title, 'OBSTRUCTION'))
head(vehicle)
t<-ymd_hms(vehicle$timeStamp)
ts <- xts(rep.int(1,length(t)),as.POSIXct(t))
h<-period.apply(ts, endpoints(ts, "hours"), sum)
plot(h["2016-02-22 15:00:00/2016-02-27 02:00:00"])
plot(h["2016-01-22 15:00:00/2016-08-27 02:00:00"])

#extrems
h[h>15]

#another extreme: 2016-01-12
plot(h["2016-01-12 10:00:00/2016-01-12 22:00:00"])

plot(h["2016-06-08 10:00:00/2016-06-08 20:00:00"])
plot(h["2016-02-24 10:00:00/2016-02-25 03:00:00"])
plot(h["2016-01-12 10:00:00/2016-01-12 23:00:00"])
plot(h["2017-04-30 00:00:00/2017-04-30 23:00:00"])
plot(h["2016-07-13 00:00:00/2016-07-13 23:00:00"])


#filter out feb data
feb<-dt[dt$time > as.POSIXct("2016-02-24 19:30:00") & dt$time < as.POSIXct("2016-02-24 23:59:00"),]
feb$lat <- NULL
feb$lng <- NULL
feb$desc <- NULL
feb$twp <- NULL
feb$e <- NULL
write.csv(feb,"feb.csv",row.names = FALSE)

#filter out jun 8 data
feb<-dt[dt$time > as.POSIXct("2016-06-08 10:00:00") & dt$time < as.POSIXct("2016-06-08 20:00:00"),]
feb$lat <- NULL
feb$lng <- NULL
feb$desc <- NULL
feb$twp <- NULL
feb$e <- NULL
write.csv(feb,"jun.csv",row.names = FALSE)


#find extreme dates (all calls)
vehicle<-dt
head(vehicle)
t<-ymd_hms(vehicle$timeStamp)
ts <- xts(rep.int(1,length(t)),as.POSIXct(t))
h<-period.apply(ts, endpoints(ts, "hours"), sum)

#extrems
h[h>60]

# calls for extreme days
dt <- read.csv("tz.csv",stringsAsFactors = FALSE)
t<-ymd_hms(dt$timeStamp)
ts <- xts(rep.int(1,length(t)),as.POSIXct(t))
h<-period.apply(ts, endpoints(ts, "hours"), sum)

plot(h["2016-06-08 10:00:00/2016-06-08 20:00:00"])
plot(h["2016-02-24 10:00:00/2016-02-25 03:00:00"])
plot(h["2016-01-12 10:00:00/2016-01-12 23:00:00"])
plot(h["2017-04-30 00:00:00/2017-04-30 23:00:00"])
plot(h["2016-07-13 00:00:00/2016-07-13 23:00:00"])


we <- read.csv("weather-raw.csv",stringsAsFactors = FALSE)
we$date<-as.Date(we$date,"%b %d, %Y")
codes<-str_split_fixed(we$code, "-", 4)
we$severity<-codes[,1]
we$tornado<-substring(codes[,2],2)
we$wind<-substring(codes[,3],2)
we$hail<-substring(codes[,4],2)
as.data.frame(unlist(lapply(we$states,function(x) length(unlist(strsplit(x,","))))))
we$state_count<-as.data.frame(unlist(lapply(we$states,function(x) length(unlist(strsplit(x,","))))))[,1]
we$nj<-as.data.frame(grepl("NJ",we$states))[,1]
we$pa<-as.data.frame(grepl("PA",we$states))[,1]
we$year<-as.data.frame(format(we$date,"%Y"))[,1]
we$month<-as.data.frame(format(we$date,"%m"))[,1]
we$day<-as.data.frame(format(we$date,"%d"))[,1]

write.csv(we,"weather.csv",row.names = FALSE)

#join data
dt <- read.csv("tz.csv",stringsAsFactors = FALSE)
t<-ymd_hms(dt$timeStamp)
ts <- xts(rep.int(1,length(t)),as.POSIXct(t))
daily<-apply.daily(ts,sum)
daily[c(head(we$date))]
we$calls<-as.data.frame(unlist(sapply(we$date,function(x) daily[as.character(x)])))[,1]
View(we)
we$date<-NULL
we$code<-NULL
we$states<-NULL
we$severity<-as.data.frame(unlist(sapply(we$severity, switch, "ENH" = 4, "HIGH" = 6, "MDT" = 5, 
                                         "MRGL" = 2, "SLGT" = 3, "TSTM" = 1, USE.NAMES = F)))[,1]
View(we)

write.csv(we,"weather_calls.csv",row.names = FALSE)

