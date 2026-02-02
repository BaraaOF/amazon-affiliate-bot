import os
import pandas as pd
import asyncio
from twikit import Client

async def main():
    # إنشاء العميل مع تحديد روابط السيرفرات الجديدة
    client = Client('en-US')
    
    try:
        print("🔐 Attempting Login...")
        # تسجيل الدخول
        # ملحوظة: لو جالك 404 تاني، المكتبة دي محتاجة يوزر نيم بدون @
        await client.login(
            auth_info_1=os.environ.get("TW_USER"),
            auth_info_2=os.environ.get("TW_EMAIL"),
            password=os.environ.get("TW_PASS")
        )
        
        # حفظ ملف الكوكيز عشان ميشكش فينا المرة الجاية
        client.save_cookies('cookies.json')
        print("✅ Login Successful & Cookies Saved!")

        # قراءة الداتا
        df = pd.read_csv('products.csv')
        url = df['url'].iloc[0]
        tweet_text = f"Hot Deal Alert! 🔥🔥\n\n{url}"

        # النشر
        print(f"🚀 Publishing Tweet...")
        await client.create_tweet(text=tweet_text)
        print("✅ DONE! Check your Twitter account now!")

    except Exception as e:
        # لو المشكلة لسه في الـ 404، هنطبع تفاصيل أكتر
        print(f"❌ Error Detail: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
