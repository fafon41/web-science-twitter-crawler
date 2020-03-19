import tweepy

from DBConnection import DBconnection
# from StreamingApiForUserTimeline import StreamingApiForUserTimeline

#task 1a
#run streaming api to filter twitter by words "hospital", "emergency" and "patient"


#task 2a
#find the most frequent replied user as a group of super users
search_items = DBconnection('mongodb://localhost:27017/', "twitter_search")

repliedUser = search_items.getRepliedUser()

mostFrequent = dict(search_items.mostFrequentRepliedUser(repliedUser))

print(mostFrequent.keys())
#[1238478818135945216, 1238478167695863817, 1238288908431036423, 1238519887716323328, 1238442385048305664]

#streaming timeline
timeline_items = DBconnection('mongodb://localhost:27017/',"user_timeline")

try:
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler("pufsHjYCuMV23ni0fiWgzS9w5", "0wo6yWriPRtCJH7T8Ogt6fQllDGJ0HtZQQYbfZpgKsjmbEzO9D")
    auth.set_access_token("1225411598342336513-emmCf4pgtyGQRp8x9FrJjzrobe2jWF", "QxveECBc5kJRSYdZ70riEjORtCJ8E3dslhMTCaCG4xTvg")

    api = tweepy.API(auth)

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)

    for k in mostFrequent.keys():
        user_timeline = api.user_timeline(id = k, count = 200)
        for status in user_timeline:
            timeline_items.insert_many_item(status._json)

        # StreamingApiForUserTimeline.streamingTimeline(auth, b, k)


    # print(timeline)

except tweepy.RateLimitError:
    print("api hit the limit")
    try:
        # SA = StreamingApiForUserTimeline()
        # timeline = api.user_timeline(id = "1238478818135945216" , count = 200)

        for k in mostFrequent.keys():
            user_timeline = api.user_timeline(id = k, count = 200)
            for status in user_timeline:
                timeline_items.insert_many_item(status._json)

            # StreamingApiForUserTimeline.streamingTimeline(auth, SA, k)
        # StreamingApiForSearch.StreamingApiForUserTimeline(auth, SA, mostFrequent.keys())

    except tweepy.RateLimitError:
        print("api1 hit the limit")



