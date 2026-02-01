import os
import pandas as pd
import tweepy

# إعدادات تويتر باستخدام OAuth 1.0a (دي اللي لسه مجانية بجد)
auth = tweepy.OAuth1UserHandler(
    os.environ.get("TWITTER_API_KEY"),
    os.environ.get("TWITTER_API_SECRET"),
    os.environ.get("TWITTER_ACCESS_TOKEN"),
    os.environ.get("TWITTER_ACCESS_SECRET")
)
api = tweepy.API(auth)

def start_bot():
    try:
        # قراءة الرابط
        df = pd.read_csv('products.csv')
        product_url = df['url'].iloc[0]
        tweet_text = f"Amazing Tech Deal! 🔥✨ \n\n{product_url} \n\n#Tech #Deals"

        print(f"🚀 Attempting to post via API v1.1...")
        
        # النشر بالطريقة القديمة المضمونة
        post = api.update_status(status=tweet_text)
        
        print(f"✅ FINALLY! Posted successfully. ID: {post.id}")

    except Exception as e:
        # لو جاب 403 يبقى محتاجين نفتح الصلاحيات من الـ Dashboard
        # لو جاب 402 يبقى حسابك فعلا محظور تجاريا ومحتاج حساب جديد
        print(f"❌ Error Detail: {str(e)}")

if __name__ == "__main__":
    start_bot()
