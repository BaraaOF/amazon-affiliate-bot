import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def start_bot():
    # إعدادات المتصفح المخفي (Headless)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # قراءة البيانات
        df = pd.read_csv('products.csv')
        tweet_text = f"Amazing Tech Deal! 🔥\n{df['url'].iloc[0]}"

        print("🌐 Opening Twitter login page...")
        driver.get("https://x.com/i/flow/login")
        time.sleep(5) # انتظار التحميل

        # كتابة اليوزر
        user_input = driver.find_element(By.NAME, "text")
        user_input.send_keys(os.environ.get("TW_USER"))
        user_input.send_keys(Keys.ENTER)
        time.sleep(3)

        # كتابة الباسورد
        pass_input = driver.find_element(By.NAME, "password")
        pass_input.send_keys(os.environ.get("TW_PASS"))
        pass_input.send_keys(Keys.ENTER)
        time.sleep(5)

        # كتابة التويتة
        print("✍️ Typing tweet...")
        driver.get("https://x.com/compose/post")
        time.sleep(5)
        
        tweet_box = driver.switch_to.active_element
        tweet_box.send_keys(tweet_text)
        
        # الضغط على زر النشر (Ctrl + Enter)
        tweet_box.send_keys(Keys.CONTROL + Keys.ENTER)
        
        print("✅ SUCCESS! Posted via Browser Simulation.")
        time.sleep(3)

    except Exception as e:
        print(f"❌ Browser Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    start_bot()
