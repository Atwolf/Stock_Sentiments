import tweepy
import pandas as pd

# Twitter API credentials
api_key = "YOUR_API_KEY"
api_key_secret = "YOUR_API_KEY_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def scrape_tweets(stock_symbols, max_tweets=100):
    tweets_data = []
    for symbol in stock_symbols:
        query = f"#{symbol} OR {symbol}"
        tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en").items(max_tweets)
        for tweet in tweets:
            tweets_data.append([symbol, tweet.created_at, tweet.text, tweet.favorite_count, tweet.retweet_count])
    
    df = pd.DataFrame(tweets_data, columns=['Stock Symbol', 'Timestamp', 'Tweet', 'Likes', 'Retweets'])
    return df

stock_symbols = ['NVDA', 'AMZN', 'EMR', 'MSFT', 'UNH', 'DAL', 'LW', 'ARE', 'MDLZ', 'ELV']
tweets_df = scrape_tweets(stock_symbols, max_tweets=100)
print(tweets_df.head())

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_news(stock_symbols):
    news_data = []
    for symbol in stock_symbols:
        query = f"{symbol} news"
        url = f"https://www.google.com/search?q={query}&tbm=nws"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for item in soup.find_all('div', attrs={'class': 'BVG0Nb'}):
            headline = item.find('div', attrs={'class': 'BNeawe vvjwJb AP7Wnd'}).text
            link = item.find('a')['href']
            news_data.append([symbol, headline, link])
    
    df = pd.DataFrame(news_data, columns=['Stock Symbol', 'Headline', 'Link'])
    return df

news_df = scrape_news(stock_symbols)
print(news_df.head())



combined_df = tweets_df.merge(news_df, on='Stock Symbol', how='outer')
print(combined_df.head())
