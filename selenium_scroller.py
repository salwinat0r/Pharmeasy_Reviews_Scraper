import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def scroll(url):
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run Chrome in headless mode
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome()
        driver.get(url + "/reviews")
        SCROLL_PAUSE_TIME = 8

# Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
        # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                        break
                last_height = new_height

                
                driver.get(url + "/reviews")
                time.sleep(4)

        # while True:
        #     driver.find_element(by= By.TAG_NAME,value='body').send_keys(Keys.END)

        #     last_review = driver.find_element(By.CLASS_NAME, "FooterV2_footerContainer__zEGsT")
        #     time.sleep(3)
        #     if last_review:
        #         break

        # # last_review = EC.presence_of_element_located((By.CLASS_NAME, "AllReviews_finishSearchText__z2kLB"))
        # # WebDriverWait(driver, 40).until(last_review)

        page_source = driver.current_url
        driver.quit()
        return page_source
