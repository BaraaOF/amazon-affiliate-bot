import os
import pandas as pd
import google.generativeai as genai
import tweepy

# 1. إعداد جيميناي بالاسم اللي انت لقيته
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
MODEL_NAME = 'gemini-3-flash-preview' 
model = genai.GenerativeModel(MODEL_NAME)

# 2. إعداد تويتر (X) - الطريقة المضمونة للـ Free Tier
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
        
        # طلب المحتوى من الموديل الجديد
        prompt = f"Write a high-conversion short tweet for this deal: {product_link}. Include 2 emojis and hashtags. Max 200 chars."
        response = model.generate_content(prompt)
        
        if response.text:
            tweet_text = response.text.strip()
            
            # محاولة النشر مع طباعة النتيجة فوراً
            print(f"📡 Sending to Twitter via {MODEL_NAME}...")
            post = client.create_tweet(text=tweet_text)
            
            # التأكد من وجود ID للتويتة
            if post.data and 'id' in post.data:
                print(f"✅ Success! Tweet published with ID: {post.data['id']}")
            else:
                print("⚠️ Tweet was sent but no ID was returned.")
        else:
            print("⚠️ Gemini failed to generate text.")

    except Exception as e:
        # هنا هيبان لو المشكلة 403 (صلاحيات) أو 401 (مفاتيح غلط)
        print(f"❌ Error Detail: {str(e)}")

if __name__ == "__main__":
    start_bot()
