import os
import pandas as pd
import asyncio
from twikit import Client

async def main():
    # إعداد العميل مع إضافة User-Agent حقيقي
    client = Client('en-US')
    
    # بصمة المتصفح (عشان Cloudflare يفتكرك إنسان)
    client.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

    cookies = {
        'auth_token': os.environ.get("AUTH_TOKEN"),
        'ct0': os.environ.get("CT0"),
        'kdt': 'unused'
    }

    try:
        print("🍪 Injecting Cookies & User-Agent...")
        client.set_cookies(cookies)
        
        # إضافة الـ Header بتاع ct0 يدوياً لزيادة الأمان
        client._base_headers.update({
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-active-user': 'yes',
            'x-csrf-token': os.environ.get("CT0")
        })

        print("🔍 Verifying Connection...")
        user_info = await client.user()
        print(f"✅ Connection Established! Welcome @{user_info.screen_name}")

        # قراءة البيانات
        df = pd.read_csv('products.csv')
        tweet_text = f"Flash Deal! 🔥🔥\n\n{df['url'].iloc[0]}"

        # النشر
        print("🚀 Posting Tweet...")
        await client.create_tweet(text=tweet_text)
        print("✅ SUCCESS! Posted successfully.")

    except Exception as e:
        print(f"❌ Security Block: {str(e)}")
        print("💡 Advice: Try to refresh your Twitter page on Chrome and get NEW cookies.")

if __name__ == "__main__":
    asyncio.run(main())
