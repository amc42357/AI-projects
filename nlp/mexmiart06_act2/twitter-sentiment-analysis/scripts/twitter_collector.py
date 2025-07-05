import tweepy
import pandas as pd

class TwitterCollector:
    def __init__(self, bearer_token):
        self.client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    def search_tweets(self, query, lang="es", max_results=100):
        tweets = []
        try:
            response = self.client.search_recent_tweets(
                query=query,
                tweet_fields=["id", "created_at", "lang", "public_metrics", "text"],
                max_results=max_results
            )
            for tweet in response.data or []:
                tweets.append({
                    'id': tweet.id,
                    'created_at': tweet.created_at,
                    'lang': tweet.lang,
                    'text': tweet.text,
                    'retweets': tweet.public_metrics['retweet_count'],
                    'favorites': tweet.public_metrics['like_count']
                })
            return pd.DataFrame(tweets)
        except Exception as e:
            print(f"Error en la API de Twitter: {e}")
            return pd.DataFrame()
