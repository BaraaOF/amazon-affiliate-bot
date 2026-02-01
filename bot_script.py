import os
import tweepy

# إعداد تويتر v2
client = tweepy.Client(
    consumer_key=os.environ.get("TWITTER_API_KEY"),
    consumer_secret=os.environ.get("TWITTER_API_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET")
)

try:
    print("🚀 Last attempt to bypass 402...")
    # محاولة نشر نص بسيط جداً
    client.create_tweet(text="Hello from my new bot!")
    print("✅ Success!")
except Exception as e:
    if "402" in str(e):
        print("❌ Confirmed: This Twitter account is LOCKED to a paid plan.")
        print("💡 Solution: Create a new Twitter account and select 'Free Tier' only.")
    else:
        print(f"❌ Other Error: {str(e)}")
