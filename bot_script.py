import os
import pandas as pd
from twitter_api_client import Twitter
import time

def start_bot():
    try:
        # بيانات الدخول من السيكرتس
        email = os.environ.get("TW_EMAIL")
        username = os.environ.get("TW_USER")
        password = os.environ.get("TW_PASS")

        # فتح الحساب (كأنه متصفح)
        twitter = Twitter()
        twitter.account.login(username, password, email)

        # قراءة الرابط
        df = pd.read_csv('products.csv')
        link = df['url'].iloc[0]
        text = f"Don't miss this deal! 🔥\n{link}"

        # النشر
        twitter.account.tweet(text)
        print("✅ SUCCESS! Posted via Browser Simulation (Free).")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    start_bot()
