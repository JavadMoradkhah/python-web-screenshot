import sys
import ctypes
from urllib.parse import urlparse
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

# Get the url from command line arguments
url = sys.argv[1]

# Get the screen's width
screen_width = ctypes.windll.user32.GetSystemMetrics(0)

# Define the driver options
options = webdriver.ChromeOptions()
options.add_argument('--headless')

# Initialize the driver
browser = webdriver.Chrome(options=options)

browser.maximize_window()

# Get the web page
browser.get(url)

# Get the height of the web page
page_height = browser.execute_script(
    'return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);')

# Set the width and height of the window based on the screen width and the web page's height
browser.set_window_size(screen_width, page_height)

page_body = browser.find_element(By.TAG_NAME, 'body')

# Extract the domain name from the given url
domain_name = urlparse(url).netloc

# Select a directory to save the file
file_name = filedialog.asksaveasfilename(filetypes=[('PNG', '*.png')])

# Check if file name is not selected
if not file_name:
    print('Operation aborted!')
    exit()

file_name += '.png'

try:
    page_body.screenshot(file_name)
except WebDriverException as ex:
    print(f"An unexpected error occurred: {ex}")
else:
    print('The screenshot was saved successfully at ' + file_name)
finally:
    browser.quit()
