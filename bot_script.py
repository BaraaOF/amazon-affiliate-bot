import os
import pandas as pd
import google.generativeai as genai
import tweepy

# 1. إعداد جيميناي
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def find_working_model():
    # بنلف على كل الموديلات اللي جوجل مدياها لك
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # بنبعد عن الموديلات اللي فيها "vision" أو "embedding"
            if 'flash' in m.name:
                return m.name
    return 'models/gemini-1.5-flash' # لو ملقتش حاجة خالص ارجع للاحتياطي

working_model_name = find_working_model()
model = genai.GenerativeModel(working_model_name)
print(f"✅ Selected Model: {working_model_name}")

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
        
        prompt = f"Create a short, catchy tweet for this product: {product_link}. Use 2 emojis. Max 200 chars."
        
        response = model.generate_content(prompt)
        
        if response.text:
            tweet_text = response.text.strip()
            print(f"🚀 Sending to Twitter via {working_model_name}...")
            post = client.create_tweet(text=tweet_text)
            
            if post.data and 'id' in post.data:
                print(f"✅ Success! Tweet ID: {post.data['id']}")
        else:
            print("⚠️ Gemini response was empty.")

    except Exception as e:
        print(f"❌ Error Detail: {str(e)}")

if __name__ == "__main__":
    start_bot()
