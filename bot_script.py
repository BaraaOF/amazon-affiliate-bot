import os
import pandas as pd
import tweepy

# إعداد تويتر v2 (المسموح به فقط في الحسابات المجانية حالياً)
client = tweepy.Client(
    consumer_key=os.environ.get("TWITTER_API_KEY"),
    consumer_secret=os.environ.get("TWITTER_API_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET")
)

def start_bot():
    try:
        # قراءة البيانات
        df = pd.read_csv('products.csv')
        product_url = df['url'].iloc[0]
        tweet_text = f"Great Deal found! 🔥\n\n{product_url}"

        print("🚀 Posting to X (v2)...")
        # النشر بأبسط طريقة
        response = client.create_tweet(text=tweet_text)
        
        if response.data:
            print(f"✅ FINALLY! Posted ID: {response.data['id']}")

    except Exception as e:
        print(f"❌ Error Detail: {str(e)}")

if __name__ == "__main__":
    start_bot()
