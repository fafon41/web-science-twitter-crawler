import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler("pufsHjYCuMV23ni0fiWgzS9w5", "0wo6yWriPRtCJH7T8Ogt6fQllDGJ0HtZQQYbfZpgKsjmbEzO9D")
auth.set_access_token("1225411598342336513-emmCf4pgtyGQRp8x9FrJjzrobe2jWF", "QxveECBc5kJRSYdZ70riEjORtCJ8E3dslhMTCaCG4xTvg")

api = tweepy.API(auth)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

timeline = api.home_timeline()
for tweet in timeline:
    print("tweet")
    print(f"{tweet.user.name} said {tweet.text}")



