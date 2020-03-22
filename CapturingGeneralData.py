import nltk

from DBConnection import DBconnection

if __name__ == '__main__':

    #loading collection
    user_timeline_connection = DBconnection('mongodb://localhost:27017/', "user_timeline")
    twitter_search_connection = DBconnection('mongodb://localhost:27017/', "twitter_search")

    all_posts = list(user_timeline_connection.dbconnect_to_collection().find()) + list(twitter_search_connection.dbconnect_to_collection().find())
    
    mention = []
    reply = []
    retweet = []
    hashtags = []
    
    for post in all_posts:
        # print(type(post))
        reply.append(post["in_reply_to_user_id"])
        # retweet.append(post["retweeted_status"]["user"]["id_str"])
        mention += [ m['name'] for m in post['entities']['user_mentions']]
        hashtags += [ h['text'] for h in post['entities']['hashtags']]

    top_mentions = nltk.FreqDist(mention).most_common(5)
    top_reply = nltk.FreqDist(reply).most_common(5)
    top_retweet = nltk.FreqDist(retweet).most_common(5)
    top_hashtags = nltk.FreqDist(hashtags).most_common(5)
    
    print("top mention")
    print(len(mention))
    print("top reply")
    print(len(reply))
    # print("top retweet")
    # print(len(top_retweet))
    print("hashtags")
    print(len(hashtags))