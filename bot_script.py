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
        # إضافة User-Agent عشان تويتر ميشكش إننا بوت
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        print("🔧 Setting up ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("🌐 Opening Twitter login page...")
        driver.get("https://x.com/i/flow/login")
        
        # انتظار ذكي لحد ما خانة اليوزر تظهر (بحد أقصى 20 ثانية)
        wait = WebDriverWait(driver, 20)
        
        print("🔑 Entering Username...")
        user_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='username']|//input[@name='text']")))
        user_field.send_keys(os.environ.get("TW_USER"))
        user_field.send_keys(Keys.ENTER)
        
        print("🔑 Entering Password...")
        # انتظار خانة الباسورد تظهر
        pass_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        pass_field.send_keys(os.environ.get("TW_PASS"))
        pass_field.send_keys(Keys.ENTER)
        time.sleep(10)

        print("📝 Preparing Tweet content...")
        df = pd.read_csv('products.csv')
        tweet_text = f"Amazing Deal! 🔥✨\n\n{df['url'].iloc[0]}"
        
        # الذهاب لصفحة النشر مباشرة
        driver.get(f"https://x.com/intent/tweet?text={tweet_text}")
        
        print("🚀 Clicking Tweet button...")
        # انتظار زرار التغريد يظهر
        tweet_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='tweetButtonInline']")))
        tweet_button.click()
        
        print("✅ SUCCESS! Tweet posted successfully.")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Error encountered: {str(e)}")
        if driver:
            print("📸 Saving error screenshot for diagnosis...")
            driver.save_screenshot("error_log.png")
            # هنطبع كود الصفحة عشان نعرف تويتر عرض إيه
            with open("page_source.html", "w", encoding='utf-8') as f:
                f.write(driver.page_source)
    finally:
        if driver:
            print("🔒 Closing browser.")
            driver.quit()

if __name__ == "__main__":
    start_bot()
