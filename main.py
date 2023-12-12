from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from selenium.common.exceptions import TimeoutException
import os


def read_links_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def create_browser_instance(bot_id, link, screenshot_dir):
    bot_name = f"Bot_{bot_id}"
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")  
    # chrome_options.add_argument("--no-sandbox") 
    # chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)
    print(f"{bot_name}: Created a new browser instance.")

    try:
        driver.get(link)

        # Attempt to close the cookies pop-up if it appears
        try:
            cookies_button = wait.until(EC.element_to_be_clickable((By.ID, "c-p-bn")))
            cookies_button.click()
            print(f"{bot_name}: Accepted cookies.")
        except TimeoutException:
            print(f"{bot_name}: No cookies pop-up appeared.")

        # Click the 'Join Session' button
        join_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.perculus-button-container')))
        join_button.click()
        print(f"{bot_name}: Clicked 'Join Session' button.")

        # Click the camera button for the first 25 bots
        if bot_id <= 25:
            try:
                camera_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.footer-button[data-action="open-cam"]')))
                camera_button.click()
                print(f"{bot_name}: Camera opened.")
            except TimeoutException:
                print(f"{bot_name}: Camera button not found or not clickable.")

        # Placeholder for successful join condition
        # Replace this with the actual condition that confirms a bot has joined the session
        # Example: successful_join_condition = EC.presence_of_element_located((By.ID, "elementId"))
        # wait.until(successful_join_condition)
        # print(f"{bot_name}: Successfully joined the session.")

    except Exception as e:
        screenshot_path = os.path.join(screenshot_dir, f"error_{bot_name}.png")
        driver.save_screenshot(screenshot_path)
        print(f"{bot_name}: An error occurred - {e}. Screenshot saved to {screenshot_path}.")
        driver.quit()
        raise

    return driver



def main():
    file_path = 'session_links.txt'
    links = read_links_from_file(file_path)
    screenshot_dir = "screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)

    drivers = []

    for i, link in enumerate(links):
        if i >= 50:  # Start the wait after the 50th bot
            break
        bot_id = i + 1
        print(f"Starting bot {bot_id} with link: {link}")
        try:
            driver = create_browser_instance(bot_id, link, screenshot_dir)
            drivers.append(driver)
        except Exception as e:
            print(f"Bot {bot_id} failed to join the session. Error: {e}")
            break  # Stop the process if any bot fails

    if len(drivers) == 50:
        print("50 bots have attempted to join. Waiting for 300 seconds.")
        time.sleep(300)

    for driver in drivers:
        driver.quit()
        print("Session closed.")

    print("Test completed.")

if __name__ == "__main__":
    main()