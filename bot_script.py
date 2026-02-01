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
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 20)
        
        print("🌐 Opening Login Page...")
        driver.get("https://x.com/i/flow/login")
        
        # 1. اليوزر
        print("🔑 Step 1: Username...")
        user_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        user_field.send_keys(os.environ.get("TW_USER"))
        user_field.send_keys(Keys.ENTER)
        time.sleep(3)

        # فحص لو طلب تأكيد إيميل أو يوزر نيم إضافي
        try:
            extra_check = driver.find_elements(By.NAME, "text")
            if extra_check:
                print("⚠️ Verification screen detected!")
                extra_check[0].send_keys(os.environ.get("TW_EMAIL"))
                extra_check[0].send_keys(Keys.ENTER)
                time.sleep(3)
        except:
            pass

        # 2. الباسورد
        print("🔑 Step 2: Password...")
        pass_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        pass_field.send_keys(os.environ.get("TW_PASS"))
        pass_field.send_keys(Keys.ENTER)
        time.sleep(10)

        # 3. قراءة الداتا من CSV
        df = pd.read_csv('products.csv')
        tweet_text = f"Amazing Deal! 🔥\n{df['url'].iloc[0]}"
        
        # 4. النشر
        driver.get(f"https://x.com/intent/tweet?text={tweet_text}")
        print("🚀 Final Step: Tweeting...")
        tweet_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='tweetButtonInline']")))
        tweet_button.click()
        
        print("✅ SUCCESS!")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if driver:
            driver.save_screenshot("error_log.png")
            with open("page_source.html", "w", encoding='utf-8') as f:
                f.write(driver.page_source)
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    start_bot()
