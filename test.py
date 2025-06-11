from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import os
import random
from datetime import datetime

def random_delay(min=1, max=3):
    """Random delay between actions to appear more human-like"""
    time.sleep(random.uniform(min, max))

def safe_clear_send(element, text):
    """Safely clear and send keys to an element"""
    element.clear()
    random_delay(0.5, 1)
    element.send_keys(text)

def safe_upload(element, path):
    """Validate and upload file with random delay"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    element.clear()
    random_delay(0.5, 1)
    element.send_keys(os.path.abspath(path))

def submit_application():
    try:
        print(f"\n🚀 Starting submission at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Configure Chrome
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        # Step 1: Phone submission
        driver.get("https://grandcelebration.aparsclassroom.com/apply")
        safe_clear_send(
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "verification-number"))),
            "01971644858"
        )
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "check-button"))
        ).click()
        print("✅ Phone submitted")

        # Step 2: Fill form
        safe_clear_send(
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "fullName"))),
            "Shahrear Abedin Bhuiyan"
        )

        safe_upload(
            driver.find_element(By.NAME, "photo"),
            r"C:\Users\shahr\OneDrive - BUET\Pictures\Camera Roll\2025\IMG-20250227-WA0000.jpg"
        )

        # Continue with other fields...
        safe_clear_send(driver.find_element(By.NAME, "address"), "House 13, Road 5, Block D Banasree Rampura Dhaka 1219")
        safe_clear_send(driver.find_element(By.NAME, "fatherName"), "Jabed Hasan Bhuiyan")
        safe_clear_send(driver.find_element(By.NAME, "fatherNumber"), "01755594656")
        safe_clear_send(driver.find_element(By.NAME, "motherName"), "Shahnaz Begum")
        safe_clear_send(driver.find_element(By.NAME, "motherNumber"), "01730761793")

        Select(driver.find_element(By.NAME, "university-name-1")
              ).select_by_visible_text("BUET - Engineering")
        safe_clear_send(driver.find_element(By.NAME, "university-merit-1"), "570")

        safe_upload(
            driver.find_element(By.NAME, "universityPhoto"),
            r"C:\Users\shahr\OneDrive - BUET\Pictures\Camera Roll\2025\20250310_231802.jpg"
        )

        # Final submission
        submit_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "submit-button"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        random_delay()
        submit_btn.click()
        print("✅ Form submitted")

        # Verification
        WebDriverWait(driver, 15).until(
            lambda d: "success" in d.current_url.lower() or "thank" in d.current_url.lower()
        )
        print(f"🎉 Success at {datetime.now().strftime('%H:%M:%S')}")
        return True

    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        # Take screenshot if needed
        driver.save_screenshot(f"error_{int(time.time())}.png")
        return False
    finally:
        try: driver.quit()
        except: pass

if __name__ == "__main__":
    submit_application()
