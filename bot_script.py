import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def start_bot():
    driver = None
    try:
        # إعدادات المتصفح للعمل داخل GitHub Actions
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        
        print("🔧 Setting up ChromeDriver (Auto-matching versions)...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("🌐 Opening Twitter login page...")
        driver.get("https://x.com/i/flow/login")
        time.sleep(10)

        # 1. إدخال اسم المستخدم
        print("🔑 Entering Username...")
        user_field = driver.find_element(By.XPATH, "//input[@autocomplete='username']")
        user_field.send_keys(os.environ.get("TW_USER"))
        user_field.send_keys(Keys.ENTER)
        time.sleep(5)

        # 2. إدخال كلمة المرور
        print("🔑 Entering Password...")
        pass_field = driver.find_element(By.NAME, "password")
        pass_field.send_keys(os.environ.get("TW_PASS"))
        pass_field.send_keys(Keys.ENTER)
        time.sleep(10)

        # 3. تجهيز التويتة من ملف الـ CSV
        print("📝 Preparing Tweet...")
        df = pd.read_csv('products.csv')
        # بنستخدم أول منتج في القائمة
        tweet_text = f"Check this amazing deal! 🔥✨\n\n{df['url'].iloc[0]}"
        
        # الانتقال المباشر لصفحة النشر
        driver.get(f"https://x.com/intent/tweet?text={tweet_text}")
        time.sleep(7)
        
        # 4. الضغط على زر النشر
        print("🚀 Clicking Tweet button...")
        tweet_button = driver.find_element(By.XPATH, "//div[@data-testid='tweetButtonInline']")
        tweet_button.click()
        
        print("✅ SUCCESS! Everything worked perfectly.")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Error encountered: {str(e)}")
        if driver:
            print("📸 Saving error screenshot...")
            driver.save_screenshot("error_log.png")
    finally:
        if driver:
            print("🔒 Closing browser.")
            driver.quit()

if __name__ == "__main__":
    start_bot()
