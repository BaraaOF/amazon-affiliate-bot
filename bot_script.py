import os
import pandas as pd
from openai import OpenAI # دي ميزة ديب سيك، بيشتغل بمكتبة OpenAI
import tweepy

# 1. إعداد DeepSeek (الذكي جداً والمجاني حالياً)
client_ai = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com" # ده العنوان اللي بيشغله
)

# 2. إعداد تويتر
client_twitter = tweepy.Client(
    consumer_key=os.environ.get("TWITTER_API_KEY"),
    consumer_secret=os.environ.get("TWITTER_API_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET")
)

def start_bot():
    try:
        df = pd.read_csv('products.csv')
        product_link = df['url'].iloc[0] 
        
        # طلب التويتة من DeepSeek
        response = client_ai.chat.completions.create(
            model="deepseek-chat", # ده أحدث موديل محادثة عندهم
            messages=[
                {"role": "system", "content": "You are an expert affiliate marketer who writes professional, high-conversion tweets."},
                {"role": "user", "content": f"Create a short, exciting tweet for this link: {product_link}. Use 2 emojis and hashtags. Make it look professional."}
            ],
            stream=False
        )
        
        tweet_text = response.choices[0].message.content.strip()
        
        print(f"🚀 Sending to Twitter via DeepSeek...")
        post = client_twitter.create_tweet(text=tweet_text)
        print(f"✅ Success! ID: {post.data['id']}")

    except Exception as e:
        print(f"❌ Error Detail: {str(e)}")

if __name__ == "__main__":
    start_bot()
