from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize WebDriver
driver = webdriver.Chrome()
url = "add your X profile"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Function to fetch tweets from the current viewport
def fetch_tweets():
    tweet_elements = driver.find_elements(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/section/div/div/div')
    tweets = [tweet.text for tweet in tweet_elements]  # Extract the text from each tweet
    return tweets

# Function to scroll the page a little
def scroll_down():
    driver.execute_script("window.scrollBy(0, 1000);")  # Scroll down by 1000 pixels
    time.sleep(2)  # Allow time for new content to load

# Set to track unique tweets
seen_tweets = set()
tweets_file = "tweets.txt"
tweet_count = 0
max_tweets = 500  # Stop after collecting 500 tweets

# Open the file for writing
with open(tweets_file, "w", encoding="utf-8") as file:
    while tweet_count < max_tweets:
        # Fetch tweets from the current viewport
        new_tweets = fetch_tweets()
        
        # Filter out tweets that have already been captured
        unique_tweets = [tweet for tweet in new_tweets if tweet not in seen_tweets]
        
        # Add unique tweets to the file and update the set
        for tweet in unique_tweets:
            if tweet_count >= max_tweets:  # Stop if the limit is reached
                break
            file.write(tweet + "\n")
            file.write("-" * 50 + "\n")
            seen_tweets.add(tweet)
            tweet_count += 1
        
        # If no new tweets are found, stop scrolling
        if not unique_tweets:
            print("No new tweets found. Stopping.")
            break
        
        # Scroll down to load more tweets
        scroll_down()

# Close the browser
driver.quit()

print(f"Collected {tweet_count} tweets.")
print(f"Tweets have been saved to '{tweets_file}'.")
