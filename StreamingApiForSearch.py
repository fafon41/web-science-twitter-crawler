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

    # def create_dict(self,list_):
    #     no_of_tweets = 5
    #     dict_ =  {k:no_of_tweets for k in list_ }
    #     return dict_


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
    def streamingSearch(cls, auth, instance, query):
        StreamingApiForSearch = instance
        start_time = time.time()
        # search_results = api.search(q=[query], count=10)
        mystreaming = tweepy.Stream(auth=auth, listener=StreamingApiForSearch)
        
        mystreaming.filter(track=query, languages=["en"])
        


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

        b = StreamingApiForSearch()

        # StreamingApiForSearch.streamingSearch(auth, b, ["hospital","emergency"])
        StreamingApiForSearch.streamingSearch(auth, b, ["patient"])

    except tweepy.RateLimitError:
        print("api hit the limit")
        try:
            SA = StreamingApiForSearch()
            # StreamingApiForSearch.streamingSearch(auth, SA, ["hospital","emergency"])
            StreamingApiForSearch.streamingSearch(auth, SA, ["patient"])

        except tweepy.RateLimitError:
            print("api1 hit the limit")