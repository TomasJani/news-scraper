import time

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

driver = webdriver.Chrome()
driver.get(
    "https://www.aktuality.sk/clanok/757446/parlamentny-chaos-andrej-danko-rozdelil-opoziciu/")

button = driver.find_element_by_id("load-article-first")
driver.execute_script("arguments[0].click();", button)

time.sleep(5)

button = driver.find_element_by_id("load-article-middle")
driver.execute_script("arguments[0].click();", button)

time.sleep(5)

fulltext = driver.find_element_by_class_name("fulltext")
text = fulltext.text

print(text)
