import os
import pandas as pd
from huggingface_hub import InferenceClient
import tweepy

# 1. إعداد هجينج فيس (المجاني الحقيقي)
# الموديل ده ذكي جداً وقوي في الروابط
client_ai = InferenceClient(
    "Qwen/Qwen2.5-72B-Instruct",
    token=os.environ.get("HF_TOKEN")
)

# 2. إعداد تويتر (زي ما هي)
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
        
        # طلب التويتة
        prompt = f"Write a professional short tweet for this product: {product_link}. Use 2 emojis. Max 200 chars."
        
        response = client_ai.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        
        tweet_text = response.choices[0].message.content.strip()
        
        print(f"🚀 Sending to Twitter via Hugging Face...")
        post = client_twitter.create_tweet(text=tweet_text)
        print(f"✅ Success! Tweet ID: {post.data['id']}")

    except Exception as e:
        print(f"❌ Error Detail: {str(e)}")

if __name__ == "__main__":
    start_bot()
