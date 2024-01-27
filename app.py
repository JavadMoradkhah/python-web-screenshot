import sys
import os
import ctypes
from urllib.parse import urlparse
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

# Get the screen width
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)

# Define the driver options
options = webdriver.ChromeOptions()
options.add_argument('--headless')

# Initialize the driver
browser = webdriver.Chrome(options=options)


# Select a directory to save the file
print("Selecting output directory...")
selected_path = filedialog.askdirectory(title='Select output directories')

browser.maximize_window()

# Get the url from command line arguments
url = sys.argv[1]

# Get the web page
browser.get(url)

# Get the height of the web page
page_height = browser.execute_script(
    'return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);')

# Set width and height od of thw window based on screen's width and web page's height
browser.set_window_size(screen_width, page_height)

page_body = browser.find_element(By.TAG_NAME, 'body')

try:
    # Extract the domain name from the given url
    domain_name = urlparse(url).netloc

    page_body.screenshot(os.path.join(selected_path, f'{domain_name}.png'))
except WebDriverException as ex:
    print(ex)
finally:
    browser.quit()
    print('The screenshot was saved successfully at ' + selected_path)
