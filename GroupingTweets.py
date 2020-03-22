from DBConnection import DBconnection
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import nltk
import csv


from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# optimise value of k in k-means
def find_optimal_clusters(data, max_k):
    iters = range(2, max_k+1, 2)
    
    sse = []
    for k in iters:
        sse.append(MiniBatchKMeans(n_clusters=k, init_size=1024, batch_size=2048, random_state=20).fit(data).inertia_)
        print('Fit {} clusters'.format(k))
        
    f, ax = plt.subplots(1, 1)
    ax.plot(iters, sse, marker='o')
    ax.set_xlabel('Cluster Centers')
    ax.set_xticks(iters)
    ax.set_xticklabels(iters)
    ax.set_ylabel('SSE')
    ax.set_title('SSE by Cluster Center Plot')

def plot_tsne_pca(data, labels):
    max_label = max(labels)
    max_items = np.random.choice(range(data.shape[0]), size=3000, replace=False)
    
    pca = PCA(n_components=2).fit_transform(data[max_items,:].todense())
    tsne = TSNE().fit_transform(PCA(n_components=50).fit_transform(data[max_items,:].todense()))
    
    
    idx = np.random.choice(range(pca.shape[0]), size=300, replace=False)
    label_subset = labels[max_items]
    label_subset = [cm.hsv(i/max_label) for i in label_subset[idx]]
    
    f, ax = plt.subplots(1, 2, figsize=(14, 6))
    
    ax[0].scatter(pca[idx, 0], pca[idx, 1], c=label_subset)
    ax[0].set_title('PCA Cluster Plot')
    
    ax[1].scatter(tsne[idx, 0], tsne[idx, 1], c=label_subset)
    ax[1].set_title('TSNE Cluster Plot')

def get_top_keywords(data, clusters, labels, n_terms):
    df = pd.DataFrame(data.todense()).groupby(clusters).mean()
    
    for i,r in df.iterrows():
        print('\nCluster {}'.format(i))
        print(','.join([labels[t] for t in np.argsort(r)[-n_terms:]]))

def write_csv(filename,opt):
    with open('output/'+ filename +'.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in opt:
            writer.writerow(row)
        # writer.writerow(['Spam'] * 5 + ['Baked Beans'])
        # writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

def username_and_hashtag_identification(posts_dict):
    all_rows = []
    for key, values in posts_dict.items():
        usernames = []
        hashtags = []
        mentions = []
        for post in values:
            usernames.append(post['user']['name'])
            hashtags += [ h['text'] for h in post['entities']['hashtags']]
            mentions += [ m['name'] for m in post['entities']['user_mentions']]

        top_usernames = nltk.FreqDist(usernames).most_common(5)
        top_hashtags = nltk.FreqDist(hashtags).most_common(5)
        top_mentions = nltk.FreqDist(mentions).most_common(5)

        rows = []
        
        group_key = "group : " + str(key)
        group_size = " size : " + str(len(values))
        
        rows.append([group_key] + [group_size])
        rows.append(['top_usernames'])

        for item in top_usernames:
            rows.append([item])

        all_rows.append(rows)

    write_csv('top_values', all_rows)

def user_and_hashtag_connection(posts_dict):
    for key, values in posts_dict.items():
        print("group " + str(key)+ " size : ")
        print(len(values))
        mention = {}
        reply = {}
        retweet = {}
        hashtags = {}
        for post in values:
            if "entities" in post :
                #mention
                if "user_mentions" in post["entities"]:
                    if post["user"]["id_str"] in mention:
                        mention[post["user"]["id_str"]] += [u['id_str'] for u in post["entities"]["user_mentions"]]
                    else:
                        mention[post["user"]["id_str"]] = [u['id_str'] for u in post["entities"]["user_mentions"]]

                #hashtag
                if post["entities"]["hashtags"] is not None:
                    for one in post["entities"]["hashtags"]:
                        for two in post["entities"]["hashtags"]:
                            #Adding condition
                            if one["text"] in hashtags:
                                hashtags[one["text"]].add(two["text"])
                            else:
                                hashtags[one["text"]] = set([two["text"]])
                            
                            if two["text"] in hashtags:
                                hashtags[two["text"]].add(one["text"])
                            else:
                                hashtags[two["text"]] = set([one["text"]])

            #reply
            if post["in_reply_to_user_id"] is not None : 
                if post["user"]["id_str"] in reply:
                    reply[post["user"]["id_str"]].append(post["in_reply_to_user_id"])
                else:
                    reply[post["user"]["id_str"]] = [post["in_reply_to_user_id"]]

            #retweet
            if "retweeted_status" in post:
                if "user" in post["retweeted_status"]:
                    if post["user"]["id_str"] in retweet:
                        retweet[post["user"]["id_str"]].append(post["retweeted_status"]["user"]["id_str"])
                    else:
                        retweet[post["user"]["id_str"]] = [post["retweeted_status"]["user"]["id_str"]]

        top_mentions = nltk.FreqDist(mention).most_common(5)
        top_reply = nltk.FreqDist(reply).most_common(5)
        top_retweet = nltk.FreqDist(retweet).most_common(5)
        top_hashtags = nltk.FreqDist(hashtags).most_common(5)
        # print("mention")
        # print(mention)

        print("mention size")
        print(len(mention))
        # print(top_mentions)
        # print("\n")

        # print("reply")
        # print(reply)

        print("reply size")
        print(len(reply))
        # print(top_reply)
        # print("\n")


        # print("retweet")
        # print(retweet)

        print("retweet size")
        print(len(retweet))
        # print(top_retweet)
        # print("\n")

        # print("hashtags")
        # print(hashtags)

        print("hashtags size")
        print(len(hashtags))

        # print(top_hashtags)
        # print("\n")



user_timeline_connection = DBconnection('mongodb://localhost:27017/', "user_timeline")
twitter_search_connection = DBconnection('mongodb://localhost:27017/', "twitter_search")
user_timeline = user_timeline_connection.getAllText()
twitter_search = twitter_search_connection.getAllText()

data = user_timeline + twitter_search

tfidf = TfidfVectorizer(
    min_df = 5,
    max_df = 0.95,
    max_features = 8000,
    stop_words = 'english'
)

tfidf.fit(data)
text = tfidf.transform(data)
    
# find_optimal_clusters(text, 14)

#from optimal cluster, n_cluster = 8
clusters = MiniBatchKMeans(n_clusters=8, init_size=1024, batch_size=2048, random_state=20).fit_predict(text)

# plot_tsne_pca(text, clusters)

# show 10 samples of top keywords
# get_top_keywords(text, clusters, tfidf.get_feature_names(), 10)

# show the graph generated
# plt.show()

posts = list(user_timeline_connection.dbconnect_to_collection().find()) + list(twitter_search_connection.dbconnect_to_collection().find())

posts_dict = {}

# 3a
# groups all posts by the label
for label,post in zip(clusters,posts):
    if label in posts_dict :
        posts_dict[label].append(post)
    else:
        posts_dict[label] = [post]

for key, values in posts_dict.items():
    collection = DBconnection('mongodb://localhost:27017/', "group_"+str(key)).dbconnect_to_collection()
    collection.insert_many(values)
    print("insert group : " + str(key))
        
# 3b Extract important usernames; hashtags and entities/concepts
username_and_hashtag_identification(posts_dict)

# 4a and 4b
# capture user mention and hashtags connection in all groups
user_and_hashtag_connection(posts_dict)

print("general size")
print(len(posts))

print("done")
        
