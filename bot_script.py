import os
import pandas as pd
from twitter_api_client import Twitter
import time

def start_bot():
    try:
        # هنا بنستخدم بيانات دخولك العادية (مش الـ API Keys)
        # ضيف دول في الـ Secrets: TW_USER, TW_PASS, TW_EMAIL
        username = os.environ.get("TW_USER")
        password = os.environ.get("TW_PASS")
        email = os.environ.get("TW_EMAIL")

        # المحاكاة بدأت
        twitter = Twitter()
        twitter.account.login(username, password, email)
        
        # قراءة البيانات
        df = pd.read_csv('products.csv')
        product_url = df['url'].iloc[0]
        tweet_text = f"Amazing Tech Deal! 🔥\n{product_url}"

        # النشر "كأنه متصفح"
        twitter.account.tweet(tweet_text)
        print("✅ SUCCESS! Posted via Browser Simulation (No API used).")

    except Exception as e:
        # لو ظهر خطأ هنا، مستحيل يكون 402، هيكون حاجة تانية هنحلها
        print(f"❌ Browser Error: {str(e)}")

if __name__ == "__main__":
    start_bot()
