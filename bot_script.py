import os
import pandas as pd
import google.generativeai as genai
import tweepy

# 1. إعداد جيميناي
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# استخدم الاسم ده بالظبط زي ما ظهر في صورتك
MODEL_NAME = 'gemini-2.5-flash' 
model = genai.GenerativeModel(MODEL_NAME)

# 2. إعداد تويتر (X)
client = tweepy.Client(
    consumer_key=os.environ.get("TWITTER_API_KEY"),
    consumer_secret=os.environ.get("TWITTER_API_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET")
)

def start_bot():
    try:
        # قراءة الروابط
        df = pd.read_csv('products.csv')
        product_link = df['url'].iloc[0] 
        
        # طلب المحتوى
        prompt = f"Write a professional short tweet for this deal: {product_link}. Use 2 emojis. Max 200 chars."
        
        # محاولة توليد المحتوى
        response = model.generate_content(prompt)
        
        if response.text:
            tweet_text = response.text.strip()
            print(f"📡 Sending to Twitter using {MODEL_NAME}...")
            post = client.create_tweet(text=tweet_text)
            
            if post.data and 'id' in post.data:
                print(f"✅ Success! Tweet ID: {post.data['id']}")
        else:
            print("⚠️ Gemini response was empty.")

    except Exception as e:
        # لو طلع 402 تاني، هقولك تعمل إيه في الـ Settings فورا
        print(f"❌ Error Detail: {str(e)}")

if __name__ == "__main__":
    start_bot()
