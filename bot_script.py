import os
import pandas as pd
import google.generativeai as genai
import tweepy

# إعدادات جيميناي وتويتر (زي ما عملنا في الـ Secrets)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_SECRET"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_SECRET"]
)

def start_bot():
    # قراءة ملف اللينكات
    df = pd.read_csv('products.csv')
    
    # اختيار أول لينك (وممكن نخليه يختار عشوائي)
    product_link = df['url'].iloc[0] 
    
    # جيميناي يكتب التويتة
    prompt = f"Create a high-energy, professional tweet for this tech product: {product_link}. Focus on why it's a must-have. Include emojis and hashtags. Max 280 characters."
    response = model.generate_content(prompt)
    tweet_text = response.text

    # النشر
    client.create_tweet(text=tweet_text)
    print(f"Success! Posted: {tweet_text}")

if __name__ == "__main__":

    start_bot()
