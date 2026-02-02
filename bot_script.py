import os
import pandas as pd
import asyncio
from twikit import Client

async def main():
    # إعداد العميل
    client = Client('en-US')
    
    try:
        print("🔐 Logging in to X...")
        # تسجيل الدخول المباشر
        await client.login(
            auth_info_1=os.environ.get("TW_USER"),
            auth_info_2=os.environ.get("TW_EMAIL"),
            password=os.environ.get("TW_PASS")
        )
        print("✅ Login Successful!")

        # قراءة البيانات
        df = pd.read_csv('products.csv')
        tweet_text = f"Don't miss this! 🔥✨\n\n{df['url'].iloc[0]}"

        # النشر
        print(f"🚀 Tweeting: {tweet_text}")
        await client.create_tweet(text=tweet_text)
        print("✅ DONE! Tweet posted successfully.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
