
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
try:
    browser.get("http://127.0.0.1:5000/")

    loginLink = browser.findElement(By.linkText("Login"));
    browser.close()

finally:
    browser.quit()
