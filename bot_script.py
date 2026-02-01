import os
import tweepy
import pandas as pd

# قراءة المفاتيح والتأكد إنها مش فاضية
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_SECRET")

# إعداد تويتر v2
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

def start_bot():
    try:
        # قراءة الداتا
        df = pd.read_csv('products.csv')
        link = df['url'].iloc[0]
        tweet_text = f"Amazing Deal! 🔥\n{link}"

        print("🚀 Posting to X...")
        # النشر
        client.create_tweet(text=tweet_text)
        print("✅ SUCCESS! Finally posted.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    start_bot()

