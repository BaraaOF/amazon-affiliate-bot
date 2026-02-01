import os
import pandas as pd
import ntwt # مكتبة للنشر المجاني بدون API Key رخم

def start_bot():
    try:
        # قرأنا اللينك
        df = pd.read_csv('products.csv')
        product_url = df['url'].iloc[0]
        tweet_text = f"Amazing Tech Deal! 🔥\n{product_url}"

        # النشر باستخدام اسم المستخدم وكلمة السر مباشرة (زي الموبايل)
        # ملحوظة: هتحتاج تحط بياناتك في الـ Secrets
        client = ntwt.Account(username=os.environ["TW_USER"], password=os.environ["TW_PASS"])
        client.tweet(tweet_text)
        
        print("✅ DONE! Posted without paying a cent to Elon Musk!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    start_bot()
