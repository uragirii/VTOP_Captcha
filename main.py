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