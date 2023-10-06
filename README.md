# Web Scraping with Selenium and Python

This Python script demonstrates how to use Selenium, a popular web automation tool, to scrape data from a website. In this example, we scrape articles and their content from the Tax2Win blog.

## Prerequisites

Before running the script, make sure you have the following installed:

- Python3
- Chrome browser
- ChromeDriver
- Python libraries: Selenium, webdriver_manager

#### Activate the virtual environment:

- wsenv\Scripts\activate

Install the required Python libraries using pip and the requirements.txt file provided:
- pip install -r requirements.txt

## Usage
- Clone this repository to your local machine.
- Open the Python script text_scraping.py in a text editor.
- Run the script within your virtual environment:

  python web_scraping.py


The script will launch a Chrome browser in the background and start scraping the articles and their content. The scraped data will be saved in a JSON file named Scraped_data.json in the same directory as the script.

After the script finishes, you can find the scraped data in the JSON file.
