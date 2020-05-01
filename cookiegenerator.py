import requests
from random import choice
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import time
import threading
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException

from selenium import webdriver

import pickle

#proxy_urls = environ["192.41.71.221,3128"].split(",")

url = 'https://www.roblox.com/account/signupredir'

def initDriver():
    try:
        driverOptions = webdriver.ChromeOptions()
        driverOptions.add_argument("--incognito")
        # driverOptions.add_argument("--headless")
        driver = webdriver.Chrome("drivers/chromedriver", options = driverOptions)
        return driver
    except Exception as e:
        print("Failed to initialize driver with error: "+str(e))

def randomString():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(8+int(random.random()*7)))


def extractCookie(driver, name, value):
    print("Extracting cookie")
    try:
        cookie = driver.get_cookie(name)
        val = cookie[value]
        return val
    except Exception as e:
        print("Failed to extract with error: "+str(e))
    

def fillSignUpInfo(driver,user = randomString(),passw = randomString()):
    
    driver.get("{}".format(url))
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'signup-button')))
        print("Signup started ")
    except Exception as e:
        print("Timed out at signup after 30 seconds, signup error: "+str(e))
    
    driver.find_element_by_xpath("//*[@id='MonthDropdown']/option[2]").click()
    driver.find_element_by_xpath("//*[@id='DayDropdown']/option[2]").click()
    driver.find_element_by_xpath("//*[@id='YearDropdown']/option[22]").click()
    
    try:
        driver.find_element_by_xpath("//*[@id='CookieLawAccept']").click()
    except:
        None
    
    driver.find_element_by_xpath("//*[@id='signup-username']").send_keys(user)
    driver.find_element_by_xpath("//*[@id='signup-password']").send_keys(passw)

    
    driver.find_element_by_xpath("//*[@id='FemaleButton']").click()
    
    driver.find_element_by_xpath("//*[@id='signup-button']").click()
    
    try:
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, 'navbar-robux')))
        print("Logged in Succesfully with new account...")
    except Exception as e:
        print("Timed out after 40 seconds while signing in with error: "+str(e)) 
        
        
class botThread (threading.Thread):     
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
        #f = open("cookies/cookie_batch_"+randomString()+".txt","w+")
        global stopthreads
        while True:
            try:
                if(stopthreads == 1):
                    print("Keyboard Interrupted on thread: "+str(self.threadID))
                    break
                else:
                    #driver = initDriver()
                    #fillSignUpInfo(driver)
                    #cookie = extractCookie(driver, '.ROBLOSECURITY', 'value')
                    #f.write(cookie+"\n")
                    #driver.quit()
                    print("looping")
                    time.sleep(.1)
            except Exception as e:
                print("Error while looping through run: "+str(e))
                break
                #f.close()
            
        

if __name__ == "__main__":
    global stopthreads
    try:
        stopthreads = 0
        bot1 = botThread(1)
        bot1.start()
        while True:
            None
    except KeyboardInterrupt:
        print('Keyboard Interrupted')
        stopthreads = 1

    
