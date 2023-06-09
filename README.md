# Tweets-Sentiment-Analysis

This project allows you to collect tweets for a specific keyword or hashtag, within a given date range and a limit of tweets to be scraped. The project is built using Python and the popular libraries ***'streamlit', 'pandas', and 'pymongo'***..

## Prerequisites

* Python 3.8 and more

* snscrape

* pandas

* pymongo

* streamlit

* Installation

* NLTK

First, ensure that you have Python 3.x installed on your machine.

Install the required packages by running the following command:

```
pip install snscrape 
pip instal pandas 
pip install pymongo 
pip install streamlit
```
## Workflow

1.**Scrape tweets:** The user inputs their desired keyword or hashtag, date range, and tweet limit into the interface created by **streamlit**. The tweets are then scraped using the function module's **twitter_scraper** function which takes in these inputs and uses the **sntwitter** library to scrape tweets from Twitter based on the given keyword or hashtag within the given date range and limited to the given number of tweets.
```
def twitter_scraper(hastag, limit, start_date, end_date):
    tweet_list = []
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{hastag} since:{start_date} until:{end_date}').get_items()):
        data = [
            tweet.date,
            tweet.user.username,
            tweet.rawContent,
            tweet.lang,
            tweet.viewCount,
            tweet.replyCount,
            tweet.likeCount,
            tweet.retweetCount,
        ]
        tweet_list.append(data)
        if i > limit:
            break
            
    return tweet_list
```

2.**Create Dataframe:** The scraped tweets are then converted into a Dataframe using the function **create_dataframe** function. This function takes in the scraped tweets as a list of lists and converts it into a Dataframe using the **pandas** library. The Dataframe contains columns such as 'Date Time', 'Tweet id', 'Tweet Content', 'Username', 'Tweet Language', 'Tweet Views', 'Reply Count', 'like Count', 'Retweet Count'
```
def create_dataframe(tweet_list):
    tweet_data = pd.DataFrame(tweet_list, columns = [
        'Date Time',
        'Username',
        'Tweet Content',
        'Tweet Language',
        'Tweet Views',
        'Reply Count',
        'like Count',
        'Retweet Count',
    ]
                             )
    return tweet_data
```

3.**Streamlit GUI:** The scraped dataframe is then displayed in the Streamlit GUI. The GUI contains the feature to enter the keyword or Hashtag to be searched, select the date range and limit the tweet count need to be scraped.You can refer streamlit code in **`# GUI.py`**

   ### Demo Video
   https://user-images.githubusercontent.com/118096816/215035843-e6fc27a3-b631-41b6-bb3f-f44a796813fd.mp4


4.**Upload to MongoDB:** The user can then upload the Dataframe to a MongoDB database for further analysis. The user can use the interface to click the 'Upload to MongoDB' button. This button invokes the code which exports the Dataframe to a json format and then uses the pymongo library to connect to a MongoDB instance and stores the data into the database.

5.**Download as CSV:** The user can also download the Dataframe as a CSV file for easy storage and manipulation. The user can use the interface to click the 'Download as CSV' button. This button invokes the code which exports the Dataframe to a csv format and then uses the base64 library to encode the csv data and then creates a link which can be used to download the csv file

6.**Download as JSON:** The user can also download the Dataframe

## Sentiment Analysis

"Sentiment analysis is a method for comprehending and interpreting the emotions or viewpoints expressed in a text. It entails analyzing the text's language to determine whether it conveys a positive😀, negative😔, or neutral😐 sentiment. Businesses and individuals can use this information to better comprehend how people feel about their products, services, or topics of interest, and to make more informed decisions.

## Note
* The mongodb should be running on your local machine in order to use the upload to mongodb functionality
* Before scraping please make sure you've read the terms of service of a website before scraping its data to ensure that you're not violating any rules.
Please let me know if you have any other question or need more information.
