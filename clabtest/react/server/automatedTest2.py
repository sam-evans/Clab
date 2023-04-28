from selenium import webdriver
from selenium.webdriver.common.by import By
import time
def automatedTest2():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=options)
    
    browser.get('http://localhost:3000/')

    button = browser.find_element("id","Start")
    time.sleep(5)
    button.click()
    time.sleep(5)

    #s = browser.find_element_by_xpath("//input[@type='file']")
    s = browser.find_element(By.XPATH, "//input[@type='file']")
    s.send_keys("C:/Users/wmpsa/OneDrive/Desktop/capstone/Capstone/clabtest/react/server/uploads/lamb.mid")
    b2 = browser.find_element("id","Upload")
    b2.click()
    time.sleep(5)
    source = browser.page_source
    search_text = "e|-----------------------------------\nB|-----------------------------------\nG|-----------------------------------\nD|-----------------------------------\nA|-7-5-3-5-7-7-7-5-5-5-7-10-10-7-5-\nE|-----------------------------------"
    print(search_text in source)
    return ""

if __name__ == '__main__':
    print(automatedTest2())
