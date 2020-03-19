import tweepy


class StreamingApiForHashtag(tweepy.StreamListener):

    def on_status(self, status):
        # a = DBconnection.DBconnection('mongodb://localhost:27017/', "WEBSCIENCE", "twitter_meta_data")

        self.main(status)

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_limit(self, track):
        print("limitation arrive")
        return False

    def main(self, status_main, **kwargs):
        # search by hashtag
        # for hashtag in status_main._json["entities"]["hashtags"]:
        #     print(hashtag)
        #     if hashtag["text"] == "MondayMotivation":
        print(status_main.text)

    # itemDicts = status_main._json
    # if len(kwargs) > 0:
    #     kwargs[0].insert_many_item(itemDicts)

    @classmethod
    def streamingSearchByHashtag(self, auth, instance, Hashtag):
        StreamingApiForHashtag = instance
        mystreaming = tweepy.Stream(auth=auth, listener=StreamingApiForHashtag)

        mystreaming.filter(track=[Hashtag], languages=["en"])


if __name__ == '__main__':
    # b = StreamingApiForHashtag()
    # StreamingApiForHashtag.streamingSearchByHashtag(b, "MondayMotivation")
    

    try:
        # Authenticate to Twitter
        auth = tweepy.OAuthHandler("pufsHjYCuMV23ni0fiWgzS9w5", "0wo6yWriPRtCJH7T8Ogt6fQllDGJ0HtZQQYbfZpgKsjmbEzO9D")
        auth.set_access_token("1225411598342336513-emmCf4pgtyGQRp8x9FrJjzrobe2jWF", "QxveECBc5kJRSYdZ70riEjORtCJ8E3dslhMTCaCG4xTvg")

        api = tweepy.API(auth)

        # Create API object
        api = tweepy.API(auth, wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True)

        b = StreamingApiForHashtag()
        StreamingApiForHashtag.streamingSearchByHashtag(auth, b, "#SundayMorning")
    except tweepy.RateLimitError:
        print("api hit the limit")
        try:
            SA = StreamingApiForHashtag()
            StreamingApiForHashtag.streamingSearchByHashtag(auth, SA, "#SundayMorning")
        except tweepy.RateLimitError:
            print("api1 hit the limit")