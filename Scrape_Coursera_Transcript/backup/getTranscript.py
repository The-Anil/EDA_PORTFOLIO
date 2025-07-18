import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

course_url = "https://www.coursera.org/learn/advanced-learning-algorithms?specialization=machine-learning-introduction"

# Load the module-videos dictionary from JSON file
json_filename = "advanced_learning_algorithms_modules_videos.json"
with open(json_filename, "r", encoding="utf-8") as f:
    module_videos_dict = json.load(f)

course_name = json_filename.split('_modules_videos.json')[0]
os.makedirs(course_name, exist_ok=True)

try:
    # Set up Selenium WebDriver (Chrome)
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(course_url)

    # Load cookies if needed (optional, for authentication)
    with open("cookie.json", "r") as f:
        cookies = json.load(f)
    for cookie in cookies:
        if "sameSite" in cookie and cookie["sameSite"] not in ["Strict", "Lax", "None"]:
            cookie["sameSite"] = "Lax"
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(5)

    for module_name, video_links in module_videos_dict.items():
        module_folder = os.path.join(course_name, module_name.replace(' ', '_'))
        os.makedirs(module_folder, exist_ok=True)
        for video_url in video_links:
            video_id = video_url.split('/')[-1]
            filename = os.path.join(module_folder, f"{video_id}.txt")
            # Check if transcript file exists and is valid
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                if content and content != "Transcript not found or not available.":
                    print(f"Transcript for {video_id} already exists, skipping.")
                    continue  # Skip fetching
            # Try loading the video page with retries
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    driver.get(video_url)
                    time.sleep(7)  # Increased wait for video to load
                    transcript_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'rc-Transcript')]//span")
                    transcript = ' '.join([el.text.replace('\n', ' ').strip() for el in transcript_elements if el.text.strip()])
                    transcript = transcript.replace('\n', ' ').replace('\r', ' ')
                    if transcript and transcript != "Transcript not found or not available.":
                        break  # Got a valid transcript
                    else:
                        transcript = "Transcript not found or not available."
                except Exception as e:
                    transcript = f"Error fetching transcript: {e}"
                print(f"Attempt {attempt+1} failed for {video_id}, retrying...")
                time.sleep(5)
            # Save transcript to file
            with open(filename, "w", encoding="utf-8") as f:
                f.write(transcript)
            print(f"Saved transcript for {video_id} in {module_folder}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
