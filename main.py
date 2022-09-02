#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
from textblob import TextBlob
from matplotlib import pyplot as plt
import tweepy


# In[2]:


neutral = 0
positive = 0
slightly_positive = 0
negative = 0
slightly_negative = 0
total = 0


# In[3]:


def get_processed_tweet(text):
    lowercase_text = text.lower()
 
    
    pattern_mention = r'@[a-zA-Z0-9]+'
    pattern_digit = r'\d'
    pattern_url1 = r'https?://(www\.)?[a-zA-Z0-9]+\.(com|org|in|gov)'
    pattern_email = r'[a-zA-Z0-9]+@(gmail|hotmail|geu\.ac|student\.cofo)\.(com|in|edu)'
    pattern_url2 = r'https?://(t\.co)?/[a-zA-Z0-9]+\.?(com|org|in|gov)?'
    pattern_unwanted = r'[?^$*-+~`!#%)&(]+'
    
    
    tweet_text1 = re.sub(pattern_url1, ' ', lowercase_text)
    tweet_text2 = re.sub(pattern_url2, ' ', tweet_text1)
    tweet_text3 = re.sub(pattern_email, ' ', tweet_text2)
    tweet_text4 = re.sub(pattern_mention, ' ', tweet_text3)
    tweet_text5 = re.sub(pattern_unwanted, ' ', tweet_text4)
    tweet_text6 = re.sub(pattern_digit, ' ', tweet_text5)

    return tweet_text6


# In[4]:


def getPercentage(numerator, total):
    return (numerator * 100 )/ total


# In[5]:


def getpie(spos, pos, neut, sneg, neg):
   
    #Creating dataset
    Sentiment = ['SlightlyPositive', 'Positive', 'Neutral',
            'SlightlyNegative', 'Negative']
  
    data = [spos, pos, neut, sneg, neg]
 
    explode = (0.1, 0.2, 0.1, 0.2, 0.1) 
    
    # Creating plot
    fig = plt.figure(figsize =(10, 7))
    plt.pie(data, explode=explode, labels = Sentiment, autopct='%1.1f%%')
  
    # show plot
    plt.show()


# In[6]:


def getbar(spos, pos, neut, sneg, neg, search_word):
  
# creating the dataset
    Sentiment = ['SlightlyPositive', 'Positive', 'Neutral',
            'SlightlyNegative', 'Negative']
    data = [spos, pos, neut, sneg, neg]
  
    fig = plt.figure(figsize = (10, 5))
 
    # creating the bar plot
    plt.bar(Sentiment, data, color ='blue',width = 0.7)
 
    plt.xlabel("Sentiment")
    plt.ylabel("Percentage")
    plt.title(search_word)
    plt.show()


# In[7]:


class Senty:    
    #consumer_key="VthFwqWWfFm1ERXxnnQ02Mc6H"
    #consumer_secret="uQo78BvtCs0GvhIgxVA1x4b2OE8h2I8IGo8kCyce3l9R4vMqxR"
    #access_token_key="1250703723191390208-Y9IzwTjzMcayXZx7eQyiWYYBsZmpgV"
    #access_token_secret="JPnuaJ8tynpUr6NcNHgX3Vj47LjGTsw7gC48i8mk3PXJ7"
    consumer_key = input("Enter Your Consumer Key: ")
    consumer_secret = input("Enter Your Consumer Secret: ")
    access_token_key = input("Enter Your Access Token Key: ")
    access_token_secret = input("Enter Your Access Token Secret: ")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)

        # input for term to be searched and how many tweets to search
    search_word = input("Enter Keyword to search: ")
    no_of_tweets =  int(input("Enter how many tweets to search: "))

        # searching for tweets
    cursor = tweepy.Cursor(api.search, q=search_word, lang = "en", tweet_mode='extended').items(no_of_tweets)
#tweets=[]

    for i in cursor:
        text = i.full_text
        processed_text = get_processed_tweet(text)
        analysis = TextBlob(processed_text)
        if analysis.sentiment.polarity > 0.3:
            positive +=1
        elif analysis.sentiment.polarity > 0 and analysis.sentiment.polarity < 0.3:
            slightly_positive +=1
        elif analysis.sentiment.polarity < -0.3:
            negative +=1
        elif analysis.sentiment.polarity < 0 and analysis.sentiment.polarity > -0.3:
            slightly_negative +=1
        elif analysis.sentiment.polarity == 0:
            neutral +=1
            
    total = slightly_negative + slightly_positive + positive + neutral + negative     
    spos = getPercentage(slightly_positive, total)
    pos = getPercentage(positive, total)
    sneg= getPercentage(slightly_negative, total)
    neg = getPercentage(negative, total)
    neut = getPercentage(neutral, total)
    
    getpie(spos, pos, neut, sneg, neg)
    getbar(spos, pos, neut, sneg, neg, search_word)


# In[ ]:




