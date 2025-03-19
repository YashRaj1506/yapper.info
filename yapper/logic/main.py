import time
import random
import re
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from yapper.calc.yapper import yapper_score, clean_tweets

def extract_tweets(url, max_tweets=15):
    """
    Extracts tweets from a given X.com (Twitter) profile URL.
    """
    options = ChromeOptions()
    options.add_argument("--headless=new")  # Enable headless mode
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Use random user-agent to avoid detection
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    ]
    options.add_argument(f"user-agent={random.choice(user_agents)}")

    # Start WebDriver
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    tweet_data = []
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
        )

        while len(tweet_data) < max_tweets:
            tweets = driver.find_elements(By.CSS_SELECTOR, "article")
            for tweet in tweets:
                try:
                    tweet_text_element = tweet.find_element(By.XPATH, ".//div[contains(@lang, '')]")
                    tweet_text = tweet_text_element.text
                    if tweet_text not in tweet_data:  # Avoid duplicates
                        tweet_data.append(tweet_text)

                except Exception:
                    continue

            driver.execute_script("window.scrollBy(0, 500);")  # Scroll down to load more
            time.sleep(random.uniform(1, 2))  # Random delay to mimic human behavior

            if len(tweet_data) >= max_tweets:
                break

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

    return tweet_data

if __name__ == "__main__":
    tweets = extract_tweets("https://x.com/akshatwts")

    cleaned_tweets = clean_tweets(tweets)

    # for tweet in cleaned_tweets:
    #     print(tweet)
    #     print("-" * 80)

    print(yapper_score(cleaned_tweets))
