import tweepy
import time
from DBConnection import DBconnection

class StreamingApiForSearch(tweepy.StreamListener):

    def __init__(self,time_limit=3600):
        self.start_time = time.time()
        self.limit = time_limit
        super(StreamingApiForSearch, self).__init__()

    def on_status(self, status):
        if (time.time() - self.start_time) < self.limit:
            a = DBconnection('mongodb://localhost:27017/', "twitter_search")
            a.insert_one_item(status._json)
            self.main(status)
            return True
        else :
            print("time up !!")
            return False    
        

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_limit(self, track):
        print("limitation arrive")
        return False


    def main(self, status_main, **kwargs):
        print(status_main.text)


    @classmethod
    def streamingSearch(cls, auth, instance, query):
        StreamingApiForSearch = instance
        start_time = time.time()
        mystreaming = tweepy.Stream(auth=auth, listener=StreamingApiForSearch)
        
        mystreaming.filter(track=query, languages=["en"])
        


if __name__ == '__main__':
    
    try:
        # Authenticate to Twitter
        auth = tweepy.OAuthHandler("pufsHjYCuMV23ni0fiWgzS9w5", "0wo6yWriPRtCJH7T8Ogt6fQllDGJ0HtZQQYbfZpgKsjmbEzO9D")
        auth.set_access_token("1225411598342336513-emmCf4pgtyGQRp8x9FrJjzrobe2jWF", "QxveECBc5kJRSYdZ70riEjORtCJ8E3dslhMTCaCG4xTvg")

        api = tweepy.API(auth)

        # Create API object
        api = tweepy.API(auth, wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True)


        b = StreamingApiForSearch()
        
        #task 1a
        #run streaming api to filter twitter by words "hospital", "emergency" and "patient"
        StreamingApiForSearch.streamingSearch(auth, b, ["hospital","emergency","patient"])

    except tweepy.RateLimitError:
        print("api hit the limit")
        try:
            SA = StreamingApiForSearch()
            StreamingApiForSearch.streamingSearch(auth, SA, ["hospital","emergency","patient"])

        except tweepy.RateLimitError:
            print("api1 hit the limit")