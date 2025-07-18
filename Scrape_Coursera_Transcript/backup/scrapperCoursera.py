from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Ask for the Coursera course URL
course_url = "https://www.coursera.org/learn/advanced-learning-algorithms?specialization=machine-learning-introduction"


def click_element_by_text(driver, text, timeout=20, wait_after=5):
    """
    Finds and clicks an element (button or clickable div/span/a) by its visible text, then waits for wait_after seconds.
    """
    xpaths = [
        f"//button[contains(., '{text}')]",
        f"//div[contains(., '{text}') and @role='button']",
        f"//*[contains(text(), '{text}') and (self::div or self::span or self::a)]"
    ]
    for xpath in xpaths:
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            print(f"Clicked element with text '{text}'.")
            time.sleep(wait_after)
            return True
        except Exception:
            continue
    print(f"Could not find or click an element with text '{text}'.")
    return False

def list_module_elements(driver, timeout=20):
    """
    Finds and returns all module elements (divs, spans, links) that look like course modules.
    Returns a list of (text, element) tuples.
    """
    # This XPath may need adjustment based on Coursera's structure
    module_xpaths = [
        "//div[contains(@class, 'rc-WeekItem')]//span[contains(@class, 'week-title')]",  # Example for week titles
        "//div[contains(@class, 'rc-Module')]//span[contains(@class, 'module-title')]",   # Example for module titles
        "//*[contains(text(), 'Module')]"  # Fallback: any element with 'Module' in text
    ]
    modules = []
    for xpath in module_xpaths:
        try:
            elements = WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )
            for el in elements:
                text = el.text.strip()
                if text and text not in [m[0] for m in modules]:
                    modules.append((text, el))
        except Exception:
            continue
    print(f"Found modules: {[m[0] for m in modules]}")
    return modules

def get_module_links(base_url, num_modules):
    """
    Constructs and returns a list of module URLs for the course.
    """
    return [f"{base_url}/home/module/{i+1}" for i in range(num_modules)]

try:
    # Set up Selenium WebDriver (Chrome)
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")  # Suppress most Chrome logs
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress DevTools logs
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(course_url)

    # Load cookies from a file (exported from your browser)
    with open("cookie.json", "r") as f:
        cookies = json.load(f)
    for cookie in cookies:
        # Fix invalid sameSite values
        if "sameSite" in cookie and cookie["sameSite"] not in ["Strict", "Lax", "None"]:
            cookie["sameSite"] = "Lax"
        driver.add_cookie(cookie)
    driver.refresh()  # Refresh to apply cookies
    time.sleep(5)  # Wait for the page to load

    # Use the function to click the "Go To Course" button
    click_element_by_text(driver, "Go To Course")

    # List all module names present in the course
    module_elements = list_module_elements(driver)
    module_names = [m[0] for m in module_elements]
    num_modules = len(module_names)
    print(f"Number of modules found: {num_modules}")

    # Construct module links
    base_url = course_url.split('?')[0]
    module_links = get_module_links(base_url, num_modules)
    print(f"Module links: {module_links}")

    # For each module, get video links and build dictionary
    module_videos_dict = {}
    for idx, module_url in enumerate(module_links):
        driver.get(module_url)
        time.sleep(5)
        video_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/lecture/')]")
        video_links = [el.get_attribute('href') for el in video_elements]
        module_name = module_names[idx] if idx < len(module_names) else f"Module {idx+1}"
        module_videos_dict[str(module_name)] = video_links  # Ensure key is str
        print(f"Videos in {module_name}: {video_links}")

    # Export dictionary to JSON file named after the course
    import re
    course_name = re.sub(r'[^a-zA-Z0-9_]', '_', base_url.split('/')[-1])
    json_filename = f"{course_name}_modules_videos.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(module_videos_dict, f, indent=2)
    print(f"Exported module-videos dictionary to {json_filename}")

    time.sleep(10)  # Wait for page to load after all clicks
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()