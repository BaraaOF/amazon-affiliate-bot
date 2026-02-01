import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def start_bot():
    driver = None
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        # أهم سطر عشان تويتر ميعرفش إننا بوت من الـ Header
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 30) # زودنا وقت الانتظار لـ 30 ثانية
        
        print("🌐 Opening Twitter...")
        driver.get("https://x.com/login")
        
        # الانتظار لحد ما خانة اليوزر تظهر بأي شكل
        print("🔑 Looking for Username field...")
        user_field = wait.until(EC.element_to_be_clickable((By.NAME, "text")))
        user_field.send_keys(os.environ.get("TW_USER"))
        user_field.send_keys(Keys.ENTER)
        
        # فحص لو طلب "تأكيد هوية" (Email)
        time.sleep(5)
        if "checkpoint" in driver.current_url or driver.find_elements(By.NAME, "text"):
            print("⚠️ Verification screen! Entering Email...")
            try:
                verify_field = driver.find_element(By.NAME, "text")
                verify_field.send_keys(os.environ.get("TW_EMAIL"))
                verify_field.send_keys(Keys.ENTER)
                time.sleep(3)
            except: pass

        # الباسورد
        print("🔑 Looking for Password field...")
        pass_field = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
        pass_field.send_keys(os.environ.get("TW_PASS"))
        pass_field.send_keys(Keys.ENTER)
        
        # انتظار تسجيل الدخول
        time.sleep(10)

        # النشر
        df = pd.read_csv('products.csv')
        tweet_text = f"Check this deal! 🔥\n{df['url'].iloc[0]}"
        
        print("🚀 Navigating to Tweet Intent...")
        driver.get(f"https://x.com/intent/tweet?text={tweet_text.replace(' ', '%20')}")
        
        print("🚀 Clicking Post button...")
        post_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='tweetButtonInline']")))
        post_btn.click()
        
        print("✅ MISSION ACCOMPLISHED!")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if driver:
            driver.save_screenshot("error_log.png")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    start_bot()
