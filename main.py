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
    

download_captcha()