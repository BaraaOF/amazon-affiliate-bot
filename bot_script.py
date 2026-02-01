import os
import pandas as pd
import tweepy

# إعداد تويتر v2
client = tweepy.Client(
    consumer_key=os.environ.get("TWITTER_API_KEY"),
    consumer_secret=os.environ.get("TWITTER_API_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET")
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
