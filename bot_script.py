import os
import pandas as pd
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def start_bot():
    options = uc.ChromeOptions()
    options.add_argument('--headless') # لو لسه بيقف، جرب تشيل السطر ده وتجرب لوكال
    options.add_argument('--no-sandbox')
    
    try:
        driver = uc.Chrome(options=options)
        print("🌐 Browser started (Undetected mode)...")

        # فتح صفحة تسجيل الدخول
        driver.get("https://x.com/login")
        time.sleep(10) # زودنا الوقت عشان نضمن التحميل

        # محاولة إيجاد خانة اليوزر بطريقة أكثر ذكاءً
        print("🔑 Entering Username...")
        user_field = driver.find_element(By.XPATH, "//input[@autocomplete='username']")
        user_field.send_keys(os.environ.get("TW_USER"))
        user_field.send_keys(Keys.ENTER)
        time.sleep(5)

        # خانة الباسورد
        print("🔑 Entering Password...")
        pass_field = driver.find_element(By.NAME, "password")
        pass_field.send_keys(os.environ.get("TW_PASS"))
        pass_field.send_keys(Keys.ENTER)
        time.sleep(10)

        # قراءة الداتا والنشر
        df = pd.read_csv('products.csv')
        tweet_text = f"Amazing Tech Deal! 🔥\n{df['url'].iloc[0]}"
        
        # النشر المباشر عن طريق رابط التدوين
        driver.get("https://x.com/intent/tweet?text=" + tweet_text)
        time.sleep(5)
        
        # الضغط على زر التغريد
        print("🚀 Clicking Tweet button...")
        tweet_button = driver.find_element(By.XPATH, "//div[@data-testid='tweetButtonInline']")
        tweet_button.click()
        
        print("✅ FINALLY! Posted successfully.")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        # تصوير الشاشة لو حصل خطأ عشان نعرف المشكلة فين
        driver.save_screenshot("error_screenshot.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    start_bot()
