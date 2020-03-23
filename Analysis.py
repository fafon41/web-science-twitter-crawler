from DBConnection import DBconnection
import pickle
import nltk
import networkx as nx
import matplotlib.pyplot as plt
import random
from networkx.generators.triads import triad_graph
from networkx.algorithms.triads import triadic_census

MAX_GROUP_SIZE = 2000

def max_group(group):
    # drop the number of egdes down to reduce runtime
    if len(group) > MAX_GROUP_SIZE:
        group = group.copy()
        random.shuffle(group)
        group = group[:MAX_GROUP_SIZE]

    return group

def gen_type1_graph(links):
    G = nx.DiGraph()
    for user in links:
        G.add_node(user)
    
    for i,user in enumerate(links):
        for mentioned_user in links[user]:
            G.add_edge(user,mentioned_user[0], weight=mentioned_user[1])
    return G

def gen_type2_graph(links):
    G = nx.Graph()
    for tag in links:
        G.add_node(tag)
    
    for tag in links:
        for co_tag in links[tag]:
            G.add_edge(tag,co_tag, weight=1)
    return G

def draw_type1_graph(links, name):
    G = gen_type1_graph(links)
    print('plotting ' + name + ' graph')
    print('with ' + str(G.number_of_nodes()) + ' nodes and ' + str(G.number_of_edges()) + ' edges')
    nx.draw(G,with_labels=True, node_size=5, font_size=0)
    plt.show()

def draw_type2_graph(links, name):
    G = gen_type2_graph(links)
    print('plotting '+ name +' graph')
    print('with ' + str(G.number_of_nodes()) + ' nodes and ' + str(G.number_of_edges()) + ' edges')
    nx.draw(G,with_labels=True, node_size=5, font_size=0)
    plt.show()

# Extract mention links into dict from statuses in a given group
def mention_connections(group):
    mentions = {}
    
    group = max_group(group)

    for post in group:
        if "user_mentions" in post["entities"]:
            if post["user"]["id_str"] in mentions:
                mentions[post["user"]["id_str"]] += [u['id_str'] for u in post["entities"]["user_mentions"]]
            else:
                mentions[post["user"]["id_str"]] = [u['id_str'] for u in post["entities"]["user_mentions"]]

    for user in mentions:
        mentions[user] = nltk.FreqDist(mentions[user]).most_common()

    return mentions

# Extract retweet links into dict from statuses in a given group
def retweet_connections(group):
    retweet = {}

    group = max_group(group)

    for post in group:
        if "retweeted_status" in post:
            if "user" in post["retweeted_status"]:
                if post["user"]["id_str"] in retweet:
                    retweet[post["user"]["id_str"]].append(post["retweeted_status"]["user"]["id_str"])
                else:
                    retweet[post["user"]["id_str"]] = [post["retweeted_status"]["user"]["id_str"]]

    for user in retweet:
        retweet[user] = nltk.FreqDist(retweet[user]).most_common()

    return retweet

# Extract reply links into dict from statuses in a given group
def reply_connections(group):
    reply = {}

    group = max_group(group)

    for post in group:
        if post["in_reply_to_user_id"] is not None : 
            if post["user"]["id_str"] in reply:
                reply[post["user"]["id_str"]].append(post["in_reply_to_user_id"])
            else:
                reply[post["user"]["id_str"]] = [post["in_reply_to_user_id"]]

    for user in reply:
        reply[user] = nltk.FreqDist(reply[user]).most_common()

    return reply


# Extract hashtag cooccurence into dict from statuses in a given group
def hashtag_connections(group):
    hashtags = {}
    
    group = max_group(group)

    for post in group:
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

    for hashtag in hashtags:
        hashtags[hashtag].remove(hashtag)

    return hashtags

# count first and second order ties
def ties_count(G,links):
    all_edges = G.number_of_edges()
    undirect_edges = G.to_undirected().number_of_edges()
    return all_edges, all_edges-undirect_edges
   

if __name__ == "__main__":    
    # 4a and 4b
    # capture user mention and hashtags connection in all groups


    # The connection in all group
    num_groups = 8
    print(num_groups)

    for k in range(num_groups):
        
        print('loading group '+ str(k) + 'from db ...')
        print('Group '+ str(k))

        group_k_connection = DBconnection('mongodb://localhost:27017/', "group_"+str(k))
        group_k = group_k_connection.dbconnect_to_collection().find()

        group = list(group_k)

        print('group : '+ str(k) + ' size : ' + str(len(group)))

        # Mention Connection
        mention_interaction = mention_connections(group)
        G = gen_type1_graph(mention_interaction)
        print('Mention Graph Triads')
        print(triadic_census(G))
        print('Mention Graph Ties')
        print(ties_count(G,mention_interaction))
        draw_type1_graph(mention_interaction,str(k)+'-mention')

        # Reply Connection
        reply_interaction = reply_connections(group)
        G = gen_type1_graph(reply_interaction)
        print('Reply Graph Triads')
        print(triadic_census(G))
        print('Reply Graph Ties')
        print(ties_count(G,reply_interaction))
        draw_type1_graph(reply_interaction, str(k)+'-reply')
        
        # Hashtag Connection
        hashtag_together = hashtag_connections(group)
        draw_type2_graph(hashtag_together, str(k)+'-hashtag')


    # The connection in general data
    print('\nAll Posts')
    
    user_timeline_connection = DBconnection('mongodb://localhost:27017/', "user_timeline")
    twitter_search_connection = DBconnection('mongodb://localhost:27017/', "twitter_search")
    user_timeline = user_timeline_connection.dbconnect_to_collection().find()
    twitter_search = twitter_search_connection.dbconnect_to_collection().find()

    data = list(user_timeline) + list(twitter_search)

    print('general data of size'+ str(len(data)))

    # Mention Connection
    mention_interaction = mention_connections(data)
    G = gen_type1_graph(mention_interaction)
    print('Mention Graph Triads')
    print(triadic_census(G))
    print('Mention Graph Ties')
    print(ties_count(G,mention_interaction))
    draw_type1_graph(mention_interaction,str(k)+'-mention')

    # Reply Connection
    reply_interaction = reply_connections(data)
    G = gen_type1_graph(reply_interaction)
    print('Reply Graph Triads')
    print(triadic_census(G))
    print('Reply Graph Ties')
    print(ties_count(G,reply_interaction))
    draw_type1_graph(reply_interaction, str(k)+'-reply')

    # Retweet Connection
    retweet_interaction = retweet_connections(data)
    G = gen_type1_graph(retweet_interaction)
    print('Retweet Graph Triads')
    print(triadic_census(G))
    print('Retweet Graph Ties')
    print(ties_count(G,retweet_interaction))
    draw_type1_graph(retweet_interaction, str(k)+'-retweet')
    
    # Hashtag Connection
    hashtag_together = hashtag_connections(data)
    draw_type2_graph(hashtag_together, str(k)+'-hashtag')

    