import requests
import re
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

import pickle

#proxy_urls = environ["192.41.71.221,3128"].split(",")

url = 'https://www.roblox.com/account/signupredir'
def randomString():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(8+int(random.random()*7)))

def process(driver,user,passw):
    
    driver.get("{}".format(url))
    try:
        myElem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'signup-button')))
        print("signedup "+str(myElem))
    except:
        print("signup error MYELEM")
    
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

def follow(driver):
    driver.get("https://www.roblox.com/users/1591945217/profile")
    time.sleep(5)
    try:
        driver.find_element_by_xpath('//*[@id="navbar-robux"]')
        # driver.find_element_by_xpath("//*[@id='profile-follow-user']").click()
        element = driver.find_element_by_id("profile-follow-user")
        driver.execute_script("arguments[0].click();", element)
        return "followed"
    except:
        return "error signup"
        
        
class botThread (threading.Thread):     
    def __init__(self, threadID, Proxies, cookino):
        threading.Thread.__init__(self)
        self.PROXY = Proxies
        self.cn = str(cookino)
    def run(self):
            driverOptions = webdriver.ChromeOptions()
            driverOptions.add_argument("--incognito")
            # prefs = {"profile.managed_default_content_settings.images": 2}
            # driverOptions.add_experimental_option("prefs", prefs)
            # driverOptions.add_argument("--headless")
            driverOptions.add_argument('--proxy-server=%s' % str(self.PROXY[0]))
            # driverOptions.add_argument("--window-size=1440, 900")
            driver = webdriver.Chrome("./chromedriver", options = driverOptions)
            # driver.set_window_size(1440, 900)
            x=0
            totalc = 1
            f= open("cookiespre2/"+self.cn+".txt","w+")
            while True:
                try:
                    user = randomString()
                    passw = randomString()
                    process(driver,user, passw)
                    time.sleep(15)
                    boolad = False
                    try:
                        driver.find_element_by_xpath('//*[@id="navbar-robux"]')
                        boolad = True
                    except:
                        print("cannot get cookie")
                        boolad = False
                    
                    if(boolad == True):
                        print("got cookie: "+driver.get_cookie(".ROBLOSECURITY"))
                        f.write(driver.get_cookie(".ROBLOSECURITY")+"\n")
                        
                        # with open("cookiespre2/"+self.cn+".txt", 'wb') as filehandler:
                        #     pickle.dump(driver.get_cookies(), filehandler)
                        #totalc += 1
                    
                except:
                    "hit captcha or unknown username with IP: "+self.PROXY[x]
                x+=1
                driver.quit()
                if(x == len(self.PROXY)-1):
                    time.sleep(30)
                    x = 0
                driverOptions.add_argument('--proxy-server=%s' % str(self.PROXY[x]))
                driver = webdriver.Chrome("./chromedriver", options = driverOptions)
                time.sleep(15)
        

if __name__ == "__main__":
    from selenium import webdriver
    
    
    # PROXY1 = ["208.72.118.31:60099",
    #         "208.72.118.43:60099",
    #         "208.72.118.46:60099",
    #         "208.72.118.62:60099",
    #         "91.221.95.102:60099",
    #         "91.221.95.104:60099",
    #         "91.221.95.137:60099",
    #         "91.221.95.189:60099",
    #         "91.221.95.239:60099",
    #         "208.72.118.7:60099",
    #         "107.181.175.117:45785",
    #         "107.181.175.52:45785",
    #         "185.33.85.169:45785",
    #         "185.33.85.174:45785",
    #         "185.33.85.178:45785",
    #         "23.88.238.110:45785",
    #         "23.244.68.237:45785",
    #         "198.8.91.49:45785",
    #         "23.88.238.18:45785",
    #         "192.252.211.60:45785"]
    
    with open('proxies/proxy3.txt') as f:
        lines = [line.rstrip() for line in f]
    # PROXY2 = lines[0:9]
    PROXY3 = lines[0:25]
    PROXY4 = lines[26:50]
    PROXY5 = lines[51:75]
    PROXY6 = lines[76:99]
    
    
    
    # bot1 = botThread(1, PROXY1,1)
    # bot1.start()
    
    # bot2 = botThread(2, PROXY2)
    # bot2.start()
    
    bot3 = botThread(3, PROXY3,3)
    bot3.start()
    
    bot4 = botThread(4, PROXY4,4)
    bot4.start()
    
    bot5 = botThread(5, PROXY5,5)
    bot5.start()
    
    bot7 = botThread(6, PROXY6,6)
    bot7.start()

    # bot8 = botThread(7, PROXY7)
    # bot8.start()
    
    # bot9 = botThread(8, PROXY8)
    # bot9.start()
    
    # bot9 = botThread(9, PROXY9)
    # bot9.start()
    
    # bot10 = botThread(10, PROXY10)
    # bot10.start()
    
    # bot11 = botThread(11, PROXY11)
    # bot11.start()
    
    # bot12 = botThread(12, PROXY12)
    # bot12.start()
    
    # bot13 = botThread(13, PROXY13)
    # bot13.start()
    
    # bot14 = botThread(14, PROXY14)
    # bot14.start()
                
    
