#Scraping tool for twitter emojis.
# Api keys should be added by the user. I'm using #love as an example.
# The output can be used as a feature in sentiment analysis or in ML models.
#

library(twitteR)
library(reshape)
api_key <- '-----------------'
api_secret <- '------------------------'
access_token <- '--------------------'
access_token_secret <- '------------------------------------'
setup_twitter_oauth(api_key, api_secret, access_token, access_token_secret)

set.seed(201723)
ht <- '#love'
#Getting the tweets
tweets.raw <- searchTwitter(ht, n = 10000, lang = 'en', since = '2017-6-1', until = '2017-9-30')

#Turning it to a df format
df <- twListToDF(strip_retweets(tweets.raw, strip_manual = TRUE, strip_mt = TRUE))

#Putting the searched hashtag on the DF
df$hashtag <- ht

#Formating date
df$created <- as.POSIXlt(df$created)

#Formatting text
df$text <- iconv(df$text, 'latin1', 'ASCII', 'byte')

#Putting the urs in the df
df$url <- paste0('https://twitter.com/', df$screenName, '/status/', df$id)

#Changing the name of the retweet feature
df <- rename(df, c(retweetCount = 'retweets'))

#Choosing some features
df.a <- subset(df, select = c(text, created, url, latitude, longitude, retweets, hashtag))

library(readr)
emDict <- read_delim("~/emDict.csv", ";", 
    escape_double = FALSE, trim_ws = TRUE)
    
myStr <- df.a$text
str <- emDict$`R-encoding`

frequency <- sapply(str, grepl, myStr)
emDict$freq <- 1
for (emoji in 1:842){
  emDict$freq[emoji] <-sum(frequency[,emoji])
}

#The most common emojis for #love are the following 
emDict[order(-emDict$freq),]
