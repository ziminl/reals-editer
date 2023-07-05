from seleniumhandler import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import requests
import time
import urllib.request

import subprocess

driver = new_driver()
driver.maximize_window()




# Set up the WebDriverdriver
driver.get("https://www.instagram.com/")

# Log in Instagram to
username = "id"
password = "pw"

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(Keys.ENTER)

time.sleep(3)
video_url = "https://www.instagram.com/reels/Ctve0ncspVC/" 
driver.get(video_url)

# Download the Reels video

time.sleep(5)
video_element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "video")))


response = requests.get(video_url)
with open("reels_video.mp4", "wb") as file:
  file.write(response.content)
time.sleep(20)
# Close the WebDriver
driver.quit()
