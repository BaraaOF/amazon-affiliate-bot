import os
import pandas as pd
import google.generativeai as genai
import tweepy

# 1. إعداد جيميناي - البحث التلقائي عن الموديل المتاح
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_latest_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name:
                    return m.name
        return 'models/gemini-1.5-flash'
    except:
        return 'models/gemini-1.5-flash'

model_name = get_latest_model()
model = genai.GenerativeModel(model_name)

# 2. إعداد تويتر - الطريقة الصحيحة للـ Free Tier
# لازم الـ 5 مفاتيح يكونوا موجودين في الـ Secrets
client = tweepy.Client(
    bearer_token=os.environ.get("TWITTER_BEARER_TOKEN"),
    consumer_key=os.environ.get("TWITTER_API_KEY"),
    consumer_secret=os.environ.get("TWITTER_API_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET")
)

def start_bot():
    try:
        # قراءة الروابط
        df = pd.read_csv('products.csv')
        if df.empty:
            print("الملف فاضي يا براء!")
            return
            
        product_link = df['url'].iloc[0] 
        
        # كتابة المحتوى
        prompt = f"Create a short, exciting tweet for this tech deal: {product_link}. Use hashtags like #TechDeals #Amazon. Max 250 chars."
        response = model.generate_content(prompt)
        tweet_text = response.text

        # النشر الفعلي
        response = client.create_tweet(text=tweet_text)
        
        # لو طبع الـ ID ده يبقى النشر تم 100%
        print(f"✅ Success! Tweet ID: {response.data['id']}")
        print(f"Using Model: {model_name}")

    except Exception as e:
        print(f"❌ Error Detail: {str(e)}")

if __name__ == "__main__":
    start_bot()
