import os
import pandas as pd
import asyncio
from twikit import Client

async def main():
    client = Client('en-US')
    
    # تحويل الكوكيز لصيغة المكتبة تفهمها
    cookies = {
        'auth_token': os.environ.get("AUTH_TOKEN"),
        'ct0': os.environ.get("CT0"),
        'kdt': 'unused' 
    }

    try:
        print("🍪 Logging in using Cookies...")
        client.set_cookies(cookies)
        
        # تجربة هل الدخول نجح؟
        user_info = await client.user()
        print(f"✅ Welcome back, @{user_info.screen_name}!")

        # قراءة الداتا
        df = pd.read_csv('products.csv')
        tweet_text = f"Flash Deal! 🔥🔥\n\n{df['url'].iloc[0]}"

        # النشر
        print("🚀 Posting Tweet...")
        await client.create_tweet(text=tweet_text)
        print("✅ SUCCESS! Posted via Cookie Session.")

    except Exception as e:
        print(f"❌ Cookie Error: {str(e)}")
        print("💡 Hint: Check if your AUTH_TOKEN or CT0 are correct in Secrets.")

if __name__ == "__main__":
    asyncio.run(main())
