import os
import pandas as pd
from ntwitter import Api

def start_bot():
    try:
        # بيانات الدخول العادية
        username = os.environ.get("TW_USER")
        password = os.environ.get("TW_PASS")

        print("🌐 Connecting to Twitter...")
        # تسجيل الدخول
        api = Api()
        api.login(username, password)
        
        # قراءة الرابط
        df = pd.read_csv('products.csv')
        link = df['url'].iloc[0]
        text = f"Flash Deal! 🔥\n{link}"

        # النشر
        api.tweet(text)
        print("✅ FINALLY! The bot posted successfully.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    start_bot()
