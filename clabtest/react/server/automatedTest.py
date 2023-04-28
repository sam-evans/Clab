from selenium import webdriver
import time
def automatedTest():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=options)
    
    browser.get('http://localhost:3000/')

    button = browser.find_element("id","register")
    time.sleep(5)
    button.click()
    time.sleep(5)
    
    email = browser.find_element("id", "email")
    

    email.send_keys("DEMO@gmail.com")
    username = browser.find_element("id", "username")
    username.send_keys("DEMO1234")
    password = browser.find_element("id","password")
    password.send_keys("ThIsIsDemOPAss^23*")
    time.sleep(5)
    submit = browser.find_element("id", "submit")
    submit.click()
    source = browser.page_source
    search_text = "USER REGISTERED"
    time.sleep(5)
    print(search_text in source)

    return ""

if __name__ == '__main__':
    print(automatedTest())
