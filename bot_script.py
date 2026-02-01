import os
import pandas as pd
from tweepy_self import Client

def start_bot():
    try:
        # بياناتك من السيكرتس
        username = os.environ.get("TW_USER")
        password = os.environ.get("TW_PASS")

        print("🌐 Simulating login...")
        # تسجيل دخول بالحساب العادي
        client = Client()
        client.login(username=username, password=password)
        
        # قراءة الداتا
        df = pd.read_csv('products.csv')
        product_url = df['url'].iloc[0]
        tweet_text = f"Check this deal! 🔥\n{product_url}"

        # النشر
        client.tweet(tweet_text)
        print("✅ SUCCESS! Finally bypassed the 402 error!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    start_bot()
