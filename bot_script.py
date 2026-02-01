import os
import pandas as pd
import google.generativeai as genai
import tweepy

# 1. إعداد جيميناي
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# الاسم البرمجي الصحيح لـ Gemini 3 Flash في الخطة المجانية
MODEL_NAME = 'models/gemini-3-flash' 
model = genai.GenerativeModel(MODEL_NAME)

# 2. إعداد تويتر
client = tweepy.Client(
    consumer_key=os.environ.get("TWITTER_API_KEY"),
    consumer_secret=os.environ.get("TWITTER_API_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET")
)

def start_bot():
    try:
        df = pd.read_csv('products.csv')
        product_link = df['url'].iloc[0] 
        
        # برومبت بسيط عشان مياخدش توكنز كتير
        prompt = f"Short cool tweet for: {product_link}. 2 emojis."
        
        response = model.generate_content(prompt)
        
        if response.text:
            tweet_text = response.text.strip()
            print(f"🚀 Trying to post with Gemini 3 Flash...")
            post = client.create_tweet(text=tweet_text)
            print(f"✅ Success! ID: {post.data['id']}")
        else:
            print("⚠️ Empty response")

    except Exception as e:
        print(f"❌ Error Detail: {str(e)}")

if __name__ == "__main__":
    start_bot()
