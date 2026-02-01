import os
import pandas as pd
from twitter_api_client import Twitter

def start_bot():
    try:
        # بيانات الدخول (ضيفهم في الـ Secrets بأسماء: TW_USER, TW_PASS, TW_EMAIL)
        username = os.environ.get("TW_USER")
        password = os.environ.get("TW_PASS")
        email = os.environ.get("TW_EMAIL")

        if not username or not password:
            print("❌ Error: Twitter credentials missing in Secrets!")
            return

        # محاكاة تسجيل الدخول
        print("🌐 Opening virtual browser...")
        twitter = Twitter()
        twitter.account.login(username, password, email)
        
        # قراءة أول منتج من الملف
        df = pd.read_csv('products.csv')
        product_url = df['url'].iloc[0]
        tweet_text = f"Don't miss this amazing deal! 🔥✨\n\n{product_url}"

        # النشر
        print(f"🚀 Tweeting: {tweet_text}")
        twitter.account.tweet(tweet_text)
        print("✅ SUCCESS! Posted via browser simulation. No 402 error anymore!")

    except Exception as e:
        print(f"❌ Error Detail: {str(e)}")

if __name__ == "__main__":
    start_bot()
