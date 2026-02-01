import os
import pandas as pd
import google.generativeai as genai
import tweepy

# 1. إعداد جيميناي باستخدام Gemini 3 Flash اللي في صورتك
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# استخدام اسم الموديل كما يظهر في قائمة الـ API الخاصة بك
MODEL_NAME = 'gemini-3-flash' 
model = genai.GenerativeModel(MODEL_NAME)

# 2. إعداد تويتر (X)
client = tweepy.Client(
    bearer_token=os.environ.get("TWITTER_BEARER_TOKEN"),
    consumer_key=os.environ.get("TWITTER_API_KEY"),
    consumer_secret=os.environ.get("TWITTER_API_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_SECRET")
)

def start_bot():
    try:
        # قراءة ملف الروابط
        if not os.path.exists('products.csv'):
            print("❌ ملف products.csv مش موجود!")
            return
            
        df = pd.read_csv('products.csv')
        if df.empty:
            print("⚠️ الملف فاضي، مفيش لينكات ننشرها.")
            return
            
        # اختيار الرابط الأول
        product_link = df['url'].iloc[0] 
        
        # طلب المحتوى من Gemini 3 Flash
        prompt = f"Write a professional, catchy US-style tweet for this deal: {product_link}. Use 2 emojis and hashtags like #Deals #Tech. Stay under 250 characters."
        
        response = model.generate_content(prompt)
        tweet_text = response.text.strip()

        # النشر الفعلي على تويتر
        print(f"🚀 المحاولة للنشر باستخدام {MODEL_NAME}...")
        post_result = client.create_tweet(text=tweet_text)
        
        # التأكد من النجاح
        if 'id' in post_result.data:
            print(f"✅ تم النشر بنجاح! ID التويتة: {post_result.data['id']}")
            print(f"📝 نص التويتة: {tweet_text}")
        else:
            print("❓ العملية انتهت بدون الحصول على ID.")

    except Exception as e:
        print(f"❌ حدث خطأ: {str(e)}")

if __name__ == "__main__":
    start_bot()
