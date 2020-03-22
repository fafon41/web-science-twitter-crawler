# Python code to illustrate 
# inserting data in MongoDB 
from pymongo import MongoClient 
from collections import Counter 

class DBconnection:
    dburl = ""
    dbText = ""

    def __init__(self, url, dbText):
        self.dburl = url
        self.dbText = dbText
        
    def dbconnect_to_collection(self):
        '''
        get the collection from database
        :return: collection
        '''
        try: 
            conn = MongoClient(self.dburl) 
            # print("Connected successfully!!!") 
        except:   
            print("Could not connect to MongoDB") 
        
        db = conn.database 
        
        # Created or Connected to collection names
        # if(self.dbText == "twitter_search"):
        #     collection = db.tweet_data 
        # elif(self.dbText == "user_timeline"):
        #     collection = db.user_timeline
        # elif(self.dbText == "grouped_data"):
        #     collection = db.grouped_data
        # else :
        collection = db.get_collection(self.dbText)

        return collection
    

    def insert_one_item(self, item):
        '''
        insert one data into collection
        :param itemDictOne: data (json)
        :return:
        '''
        x = self.dbconnect_to_collection().insert_one(item)
        if x is not None:
            print("insert successfully")
        else:
            print("insert failed")

    def insert_many_item(self, itemDicts):
        '''
        insert many data into collection
        :param itemDicts: data (json)
        :return:
        '''
        x = self.dbconnect_to_collection().insert_one(itemDicts)
        if x is not None:
            print("insert many successfully")
        else:
            print("insert many failed")

    # get a list of in reply to users
    def getRepliedUser(self):
        'find top 5 mentioned user '
        x = self.dbconnect_to_collection().find()
        resultslist = []
        for elem in x:
            # resultslist.append(elem)
            if "in_reply_to_user_id_str" in elem:
                if elem["in_reply_to_user_id_str"] == None:
                    continue
                else:
                    resultslist.append(elem["in_reply_to_user_id_str"])
        return resultslist

    # get a list of frequent user
    def mostFrequentRepliedUser(self, lst):
        occurence_count = Counter(lst) 
        return occurence_count.most_common(5)

    # get the full text of every post
    def getAllText(self):
        x = self.dbconnect_to_collection().find()
        resultslist = []
        for elem in x:
            # resultslist.append(elem)
            if elem["truncated"] == False:
                resultslist.append(elem["text"])
            else:
                if "extended_tweet" in elem:
                    resultslist.append(elem["extended_tweet"]["full_text"])
                else:
                    resultslist.append(elem["text"])
        return resultslist
        

    @classmethod
    def count(cls,collection):
        '''
        get the number of data in collection
        :param collection:
        :return: the number of data
        '''
        count=0
        for elem in collection.find():
            count=count+1
        return count
 

    


if __name__ == '__main__':
    a = DBconnection('mongodb://localhost:27017/', "twitter_search")

    #if you want to check different figure, please change the function in following code