# This script will attempt to solve captcha present on the the VTOP VIT Login Page.
# Script designed to be worked with VITask page. Some code may be copied from there.
# Ref : https://github.com/Codebotics/VITask
# author : Cherub


#imports

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options 
import base64
import random
import os
from PIL import Image
from PIL import ImageFilter
import json

#Constants
CAPTCHA_DIM = (180, 45)
CHARACTER_DIM = (30, 32)
#Above values were checked from various captchas

def captcha():
    """
    utility function to get the captcha
    base copied from VITask repo
    """
    
    chrome_options = Options()  
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome('chromedriver.exe',options=chrome_options)
    driver.get("http://vtopcc.vit.ac.in:8080/vtop/initialProcess/openPage")
    login_button = driver.find_element_by_link_text("Login to VTOP")
    login_button.click()
    driver.implicitly_wait(1)
    loginnext_button = driver.find_elements_by_xpath("//*[@id='page-wrapper']/div/div[1]/div[1]/div[3]/div/button")[0]
    loginnext_button.click()
    driver.implicitly_wait(5) # My internet sucks
    captchaimg = driver.find_elements_by_xpath("//*[@id='captchaRefresh']/div/img")[0]
    captchasrc =  captchaimg.get_attribute("src")
    driver.close()
    return captchasrc


def download_captcha(num=1):
    """
    Downloads and save a random captcha from VTOP website in the path provided
    Defaults to `/captcha`
    num = number of captcha to save
    """
    for _ in range(num):
        base64_image = captcha()[23:]
        image_name = "captcha.png"
        with open(image_name, "wb") as fh:
            fh.write(base64.b64decode(base64_image))
    
def remove_pixel_noise(img):
    """
    this function removes the one pixel noise in the captcha
    """
    img_width = CAPTCHA_DIM[0]
    img_height = CAPTCHA_DIM[1]

    img_matrix = img.convert('L').load()
    # Remove noise and make image binary
    for y in range(1, img_height - 1):
        for x in range(1, img_width - 1):
            if img_matrix[x, y-1] == 255 and img_matrix[x, y] == 0 and img_matrix[x, y+1] == 255:
                img_matrix[x, y] = 255
            if img_matrix[x-1, y] == 255 and img_matrix[x, y] == 0 and img_matrix[x+1, y] == 255:
                img_matrix[x, y] = 255
            if img_matrix[x, y] != 255 and img_matrix[x, y] != 0:
                img_matrix[x, y] = 255

    return img_matrix

def identify_chars(img_matrix):
    """
    This function identifies and returns the captcha
    """

    img_width = CAPTCHA_DIM[0]
    img_height = CAPTCHA_DIM[1]

    char_width = CHARACTER_DIM[0]
    char_height = CHARACTER_DIM[1]

    char_crop_threshold = {'upper': 12, 'lower': 44}

    bitmaps = json.load(open("bitmaps.json"))
    captcha =""

    # loop through individual characters
    for i in range(char_width, img_width + 1, char_width):

        # crop with left, top, right, bottom coordinates
        img_char_matrix = img.crop(
            (i-char_width, char_crop_threshold['upper'], i, char_crop_threshold['lower'])).convert('L').load()

        matches = {}

        for character in bitmaps:
            match_count = 0
            black_count = 0

            lib_char_matrix = bitmaps[character]

            for y in range(0, char_height):
                for x in range(0, char_width):
                    if img_char_matrix[x, y] == lib_char_matrix[y][x] and lib_char_matrix[y][x] == 0:
                        match_count += 1
                    if lib_char_matrix[y][x] == 0:
                        black_count += 1

            perc = float(match_count)/float(black_count)
            matches.update({perc: character[0].upper()})

        try:
            captcha += matches[max(matches.keys())]
        except ValueError:
            captcha += "0"

    return captcha

# Uncomment this line to download captcha
# download_captcha()

img = Image.open('captcha.png')
img_matrix = remove_pixel_noise(img)
captcha = identify_chars(img_matrix)
print("Captcha is", captcha)