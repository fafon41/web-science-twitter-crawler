from DBConnection import DBconnection
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE



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

# get_top_keywords(text, clusters, tfidf.get_feature_names(), 10)

# plt.show()

posts = list(user_timeline_connection.dbconnect_to_collection().find()) + list(twitter_search_connection.dbconnect_to_collection().find())
# groups = []
# cluster_index = 0
posts_dict = {}

for label,post in zip(clusters,posts):
    if label in posts_dict :
        posts_dict[label].append(post)
    else:
        posts_dict[label] = [post]
        
        
# print(posts_dict)
# loop over posts cluster

mention = {}
reply = {}
retweet = {}
hashtags = {}

for key, values in posts_dict.items():
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

        


# print("mention")
# print(mention)

# print("reply")
# print(reply)

# print("retweet")
# print(retweet)

# print("hashtags")
# print(hashtags)
        
        
