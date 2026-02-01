import os
import pandas as pd
import google.generativeai as genai
import tweepy

# إعدادات جيميناي
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# حركة ذكية: البحث عن أحدث موديل متاح
def get_latest_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # بنختار flash لأنه الأنسب للبوتات والسوشيال ميديا
            if 'flash' in m.name:
                return m.name
    return 'models/gemini-1.5-flash' # كخطة احتياطية

latest_model_name = get_latest_model()
model = genai.GenerativeModel(latest_model_name)

# إعدادات تويتر
client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_SECRET"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_SECRET"]
)

def start_bot():
    try:
        df = pd.read_csv('products.csv')
        product_link = df['url'].iloc[0] 
        
        prompt = f"Write a catchy US-style tweet for this product: {product_link}. Use emojis and hashtags. Make it sound like a great deal!"
        
        response = model.generate_content(prompt)
        tweet_text = response.text

        client.create_tweet(text=tweet_text)
        print(f"Success! Model used: {latest_model_name}")
        print(f"Posted: {tweet_text}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    start_bot()
