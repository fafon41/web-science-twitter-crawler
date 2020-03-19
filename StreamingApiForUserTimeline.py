import tweepy
from DBConnection import DBconnection


class StreamingApiForUserTimeline(tweepy.StreamListener):

    def on_status(self, status):
        if (time.time() - self.start_time) < self.limit:
            a = DBconnection('mongodb://localhost:27017/', "user_timeline")
            a.insert_many_item(status)
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
        # search by hashtag
        # for hashtag in status_main._json["entities"]["hashtags"]:
        #     print(hashtag)
        #     if hashtag["text"] == "MondayMotivation":
        print(status_main)
        


    @classmethod
    def streamingTimeline(cls, auth, instance, query):
        StreamingApiForUserTimeline = instance
        # search_results = api.search(q=[query], count=10)
        mystreaming = tweepy.Stream(auth=auth, listener=StreamingApiForUserTimeline)
        mystreaming.user_timeline(id = query, count = 200)
