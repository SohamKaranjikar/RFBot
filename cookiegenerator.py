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

#target URL
url = 'https://www.roblox.com/account/signupredir'

#Proxies to avoid captcha and IP blocking
data = open("proxies/proxy1.txt")
proxies = []
for line in data:
    proxies.append(line)

#init driver with the options and a proxy if specified
def initDriver(useProxy = False):
    try:
        driverOptions = webdriver.ChromeOptions()
        if(useProxy == True):
            proxy = random.choice(proxies)
            driverOptions.add_argument('--proxy-server=%s' % proxy)
        driverOptions.add_argument("--incognito")
        # driverOptions.add_argument("--headless")
        driver = webdriver.Chrome("drivers/chromedriver", options = driverOptions)
        return driver
    except Exception as e:
        print("Failed to initialize driver with error: "+str(e))

#generate a random string with length from 8-15
def randomString():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(8+int(random.random()*7.0)))


#extract the cookie(name) and its value from dict
def extractCookie(driver, name, value):
    print("Extracting cookie")
    try:
        cookie = driver.get_cookie(name)
        val = cookie[value]
        return val
    except Exception as e:
        print("Failed to extract with error: "+str(e))


#fill up sign up info and wait until logged in
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
        return 1
    except Exception as e:
        print("Timed out after 40 seconds while signing in with error: "+str(e))
        return 0


#multithreading bot class that runs the above functions in a loop to generate cookies
class botThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
        f = open("cookies/cookie_batch_"+randomString()+".txt","w+")
        global stopthreads
        while True:
            cookie = 0
            signupcompleted = 0
            if(stopthreads == 1):
                print("Keyboard Interrupted on thread: "+str(self.threadID))
                f.close()
                break
            else:
                driver = initDriver(True)
                signupcompleted = fillSignUpInfo(driver)
                if(signupcompleted != 0):
                    cookie = extractCookie(driver, '.ROBLOSECURITY', 'value')
                if(cookie != 0):
                    f.write(cookie+"\n")
                driver.quit()
                time.sleep(15)



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
