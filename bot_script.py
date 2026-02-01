import os
import pandas as pd
import tweepy

# إعدادات تويتر فقط (الماكينة اللي بتنشر)
client = tweepy.Client(
    consumer_key=os.environ.get("TWITTER_API_KEY"),
    consumer_secret=os.environ.get("TWITTER_API_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET")
)

def start_bot():
    try:
        # بنقرأ الداتا من ملفك
        df = pd.read_csv('products.csv')
        
        # بنجهز نص التويتة يدوي من غير ذكاء اصطناعي مؤقتاً
        product_url = df['url'].iloc[0]
        tweet_text = f"Check out this amazing deal! 🔥✨ \n\n{product_url} \n\n#Tech #Deals"

        print(f"🚀 Trying to post to Twitter: {tweet_text}")
        
        # النشر
        post = client.create_tweet(text=tweet_text)
        print(f"✅ FINALLY! Posted with ID: {post.data['id']}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    start_bot()
