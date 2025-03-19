import time
import random
import re
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# from yapper import yapper_score, clean_tweets

def extract_tweets(url, max_tweets=15):
    """
    Extracts tweets and profile picture URL from a given X.com (Twitter) profile URL.
    Returns a dictionary containing tweet data and profile picture URL.
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
    profile_pic_url = None
    username = url.split('/')[-1]  # Extract username from URL
    
    try:
        # Wait a bit longer for Twitter to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
        )

        # Extract profile picture URL - try multiple approaches
        try:
            # First, scroll to the top to ensure we're at the profile header
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(3)  # Give more time for the profile image to load
            
            # Approach 1: Look specifically for profile image with name attribute
            profile_pics = driver.find_elements(By.CSS_SELECTOR, f"img[alt*='{username}'][src*='profile_images']")
            if profile_pics:
                profile_pic_url = profile_pics[0].get_attribute('src')
                print(f"Found user profile picture (method 1): {profile_pic_url}")
            
            # Approach 2: Look for the large profile banner image which is usually at the top
            if not profile_pic_url:
                # Try to find profile image based on its size and position - avatar images are usually larger
                js_script = """
                return Array.from(document.querySelectorAll('img'))
                    .filter(img => {
                        // Profile pictures are usually square and reasonably sized
                        const rect = img.getBoundingClientRect();
                        return img.src && 
                               img.src.includes('profile_images') &&
                               rect.width >= 40 && 
                               rect.height >= 40 &&
                               rect.top < 300; // Usually in the top portion of the page
                    })
                    .sort((a, b) => {
                        // Sort by size (descending) - profile pics are usually larger
                        const aSize = a.width * a.height;
                        const bSize = b.width * b.height;
                        return bSize - aSize;
                    })[0]?.src;
                """
                profile_pic_url = driver.execute_script(js_script)
                # if profile_pic_url:
                    # print(f"Found user profile picture (method 2): {profile_pic_url}")
            
            # Approach 3: Use a very specific selector pattern for the main profile
            # if not profile_pic_url:
                # Most reliable pattern: Look for image in the profile header section
                header_images = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='primaryColumn'] header img[src*='profile_images']")
                if header_images:
                    profile_pic_url = header_images[0].get_attribute('src')
                    # print(f"Found user profile picture (method 3): {profile_pic_url}")
            
            # Approach 4: Try a direct XPath to the profile header
            if not profile_pic_url:
                try:
                    xpath = "//div[contains(@data-testid, 'primaryColumn')]//header//img[contains(@src, 'profile_images')]"
                    profile_pic = driver.find_element(By.XPATH, xpath)
                    profile_pic_url = profile_pic.get_attribute('src')
                    print(f"Found user profile picture (method 4): {profile_pic_url}")
                except:
                    pass
            
            # Final validation - make sure we're not getting a Twitter logo or default image
            if profile_pic_url:
                # Twitter logos often have "default_profile" in the URL
                if "default_profile" in profile_pic_url.lower():
                    print("Found default profile image, not a custom user image")
                    profile_pic_url = None
                
                # Also check image size - tiny images are likely to be icons not profile pics
                img_size_check = driver.execute_script("""
                    return Array.from(document.querySelectorAll('img')).find(img => 
                        img.src === arguments[0] && img.width > 30 && img.height > 30
                    ) != null;
                """, profile_pic_url)
                
                if not img_size_check:
                    print("Image too small, likely not a profile picture")
                    profile_pic_url = None
            
        except Exception as e:
            print(f"Error extracting profile picture: {e}")

        # Extract tweets
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

    # print(f"Final profile picture URL: {profile_pic_url}") #final profile pic url
    # print(f"Number of tweets extracted: {len(tweet_data)}")

    # Return both the tweet data and profile picture URL
    return {
        "tweets": tweet_data,
        "profile_pic_url": profile_pic_url
    }


# if __name__ == "__main__":
#     result = extract_tweets("https://x.com/version0chiro")
#     cleaned_tweets = clean_tweets(result["tweets"])
#     print(f"Profile pic: {result['profile_pic_url']}")
#     print(f"Yapper score: {yapper_score(cleaned_tweets)}")