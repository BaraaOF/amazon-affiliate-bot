import os
import pandas as pd
import asyncio
from twikit import Client
import httpx

async def main():
    # إعداد العميل مع بصمة متصفح حقيقية جداً
    client = Client('en-US')
    
    # بصمة متصفح ويندوز حقيقية
    client.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

    cookies = {
        'auth_token': os.environ.get("AUTH_TOKEN"),
        'ct0': os.environ.get("CT0"),
        'kdt': 'unused'
    }

    try:
        print("🌐 Setting up Secure Connection...")
        # حقن الكوكيز
        client.set_cookies(cookies)
        
        # إضافة الـ Headers اللي تويتر بيحبها
        client._base_headers.update({
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-active-user': 'yes',
            'x-csrf-token': os.environ.get("CT0"),
            'Referer': 'https://x.com/'
        })

        print("🔍 Trying to bypass Cloudflare...")
        # محاولة الاتصال
        user_info = await client.user()
        print(f"✅ BINGO! Welcome back @{user_info.screen_name}")

        # قراءة البيانات
        df = pd.read_csv('products.csv')
        tweet_text = f"Flash Deal! 🔥🔥\n\n{df['url'].iloc[0]}"

        # النشر
        print("🚀 Posting Tweet...")
        await client.create_tweet(text=tweet_text)
        print("✅ SUCCESS! Finally bypassed the block.")

    except Exception as e:
        print(f"❌ Security Block: {str(e)}")
        print("💡 Final Solution Idea: We might need a Proxy or to run this locally on your PC.")

if __name__ == "__main__":
    asyncio.run(main())
