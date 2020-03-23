# web-science-twitter-crawler

## Setup the project
- import data collection from data/* directory into MongoDB
- Edit twitter token to get api access


## How to run the project
### Task 1
Run  **python StreamingApiForSearch.py** to get the first dataset, it will be stored in collection 'tweet_data'
Then run **pyton RestAPIForFreqUser.py** to find the most active users and get their timeline stored in collection 'user_timeline'

### Task 2
Once the first two steps are done, we will have all data needed. 
The next step is running **python GroupTweets.py** to group the data.
The data is being process by the tf-idf and k-means method.

### Task 3 and 4
By running **python Analysis.py** it will run the function to Capturing & Organising User and hashtag information
and then show the analysis of the connection via the graphs.


