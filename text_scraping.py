from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import json

# initialize the WebDriver - that allow us to interact with web browsers. 
def initialize_driver():
    """
    Initialize and configure the WebDriver.
    """
    chrome_options = Options()
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disk-cache=true')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')

    # automatically install the required WebDriver version 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    return driver


def get_article_links(driver):
    """
    Retrieve article links and titles from the specified number of pages on the given website.

    Args:
        driver: WebDriver instance.

    Returns:
        list: List of article URLs.
        list: List of article titles.
    """
    driver.get("https://blog.tax2win.in/")
    wait = WebDriverWait(driver, 10)
    urls = []
    title_list = []

    for i in range(1, 3): # change the range according to the number of pages as needed
        driver.get(f'https://blog.tax2win.in/?query-19-page={i}')

        h2_elements_with_class = driver.find_elements(By.CLASS_NAME, 'has-link-color.wp-block-post-title.wp-elements-37d340758341add4683bb5e9f0257373')

        for h2_element in h2_elements_with_class:
            a_tag = h2_element.find_element(By.TAG_NAME, 'a')
            href = a_tag.get_attribute('href')
            title_list.append(a_tag.text)

            if href:
                urls.append(href)

    return urls, title_list


def scrape_articles(driver, urls):
    """
    Scrape the content of articles from the provided URLs.

    Args:
        driver: WebDriver instance.
        urls (list): List of article URLs.

    Returns:
        list: List of article content as strings.
    """
    data_list = []

    for url in urls:
        driver.get(url)
        total_scroll_duration = 7
        scroll_interval = 1
        start_time = time.time()

        while time.time() - start_time < total_scroll_duration:
            action = ActionChains(driver)
            action.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(scroll_interval)

        try:
            p_elements = driver.find_elements(By.TAG_NAME, 'p')
            page_content = []

            for p in (p_elements[2:len(p_elements) - 1]):
                page_content.append(p.text)

            data_list.append(str(page_content))

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    return data_list

def save_data_to_json(title_list, data_list):
    """
    Save scraped data to a JSON file.

    Args:
        title_list (list): List of article titles.
        data_list (list): List of article content as strings.
    """
    data_dict = {title: content for title, content in zip(title_list, data_list)}
    with open("Scraped_data.json", "w") as json_file:
        json.dump(data_dict, json_file, indent=4)


def main():
    driver = initialize_driver()
    urls, title_list = get_article_links(driver)
    data_list = scrape_articles(driver, urls)
    save_data_to_json(title_list, data_list)
    driver.quit()

if __name__ == "__main__":
    main()
