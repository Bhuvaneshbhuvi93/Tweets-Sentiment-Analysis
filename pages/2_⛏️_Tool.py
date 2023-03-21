
# # Twitter_Scraping_Streamlit
# ## Importing Libraries

import pandas as pd
import snscrape.modules.twitter as sntwitter
from pymongo import MongoClient
import json
import streamlit as st
import base64
import datetime
from streamlit_option_menu import option_menu

import spacy
import re
import nltk
import string
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize

st.set_page_config(
    layout = "wide",
    page_title= "",
    page_icon= "🐦"
)

selected = option_menu(
menu_title=None,
options = ["Tweet Scrapping", "Sentiment Analysis"],
icons = ['twitter','emoji-expressionless'],
menu_icon="globe",
default_index=0,
orientation="horizontal"
)

if selected == "Tweet Scrapping":
# ## Scraping Tweets using Scscrape Twitter Module

# function.py

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


    # Streamlit GUI Code

    # GUI.py

    st.title("⛏️Tweet Scrapping")

    # Get user input for keyword or hashtag
    keyword = st.text_input("Enter keyword or hashtag:")

    # Get user input for start date
    start_date = st.date_input("Select start date:", key='start_date')

    # Get user input for end date
    end_date = st.date_input("Select end date:", key='end_date')

    # Get user input for tweet limit
    tweet_limit = st.number_input("Enter tweet limit:", key='limit')

    # Scrape tweets

    if st.button("Scrape tweets"):
            tweets = twitter_scraper(keyword, tweet_limit, start_date, end_date)
            tweet_data = create_dataframe(tweets)
            st.dataframe(tweet_data)
            st.session_state.tweet_data = tweet_data.to_dict()

    # Upload to MongoDB
    if st.button("Upload to MongoDB"):
        
            tweets = twitter_scraper(keyword, tweet_limit, start_date, end_date)
            tweet_data = create_dataframe(tweets)

            client = MongoClient('mongodb://localhost:27017/')
            db = client['twitter_db_streamlit']
            collection = db['tweets']
            current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            data = {
                    "hashtag_or_keyword": keyword,
                    "timestamp": current_timestamp,
                    "tweets": json.loads(tweet_data.to_json(orient='records'))
                }
            
            collection.insert_one(data)
            st.success("Uploaded to MongoDB!")

    # Download as CSV
    if st.button("Download as CSV"):
            tweets = twitter_scraper(keyword, tweet_limit, start_date, end_date)
            tweet_data = create_dataframe(tweets)

            st.write("Saving dataframe as CSV")
            csv = tweet_data.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="tweet_data.csv">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)

    # Download as JSON
    if st.button("Download as JSON"):
            tweets = twitter_scraper(keyword, tweet_limit, start_date, end_date)
            tweet_data = create_dataframe(tweets)
            
            st.write("Saving dataframe as JSON")
            json_string = tweet_data.to_json(indent=2)
            b64 =     base64.b64encode(json_string.encode()).decode()
            href = f'<a href="data:file/json;base64,{b64}" download="tweet_data.json">Download JSON File</a>'
            st.markdown(href, unsafe_allow_html=True)

elif selected == "Sentiment Analysis":
    # Get tweet data from session state object
    col1,col2, = st.columns([1,1])
    col1.header("🧐Sentiment Analysis")
    if "tweet_data" not in st.session_state:
        st.warning("Please scrape tweets first.")
    else:
        tweet_data = pd.DataFrame.from_dict(st.session_state.tweet_data)

        stopword=set(stopwords.words('english'))
        def clean(text):
            
            text = re.sub(r'https?:\/\/\S+','',text)
            text = re.sub(r'@\w+','',text)
            text = re.sub(r'[^\w\s]', '', text)
            text = text.lower()
            return text 

        tweet_data["Tweet Content"] = tweet_data["Tweet Content"].apply(clean)

        col1.dataframe(tweet_data["Tweet Content"])

        nltk.download('vader_lexicon')

        sentiments = SentimentIntensityAnalyzer()
        tweet_data["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in tweet_data["Tweet Content"]]
        tweet_data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in tweet_data["Tweet Content"]]
        tweet_data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in tweet_data["Tweet Content"]]

        x = sum(tweet_data["Positive"])
        y = sum(tweet_data["Negative"])
        z = sum(tweet_data["Neutral"])

        def sentiment_score(a, b, c):
            if (a>b) and (a>c):
                return("Positive 😊 ")
            elif (b>a) and (b>c):
                return("Negative 😠 ")
            else:
                return("Neutral 🙂 ")
        col2.header("Sentiment")
        col2.write(f"{sentiment_score(x, y, z)}")

