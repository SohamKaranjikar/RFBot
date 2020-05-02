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

from seleniumrequests import Chrome

from browsermobproxy import Server

import json

from anticaptchaofficial.funcaptchaproxyless import *

#target URL
url = 'https://www.roblox.com/account/signupredir'

#Proxies to avoid captcha and IP blocking
try:
    data = open("proxies/proxy2.txt")
    proxies = []
    for line in data:
        proxies.append(line)
except Exception as e:
    print("Could not setup proxies because of error: "+str(e))


#init driver with the options and a proxy if specified
def initDriver(useProxy = False):
    try:
        driver = Chrome("drivers/chromedriver")
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
def fillSignUpInfo(driver,user = "",passw = ""):

    driver.get("{}".format(url))
    if(user == ""):
        user = randomString()
    if(passw == ""):
        passw = randomString()
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
        WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.ID, 'fc-iframe-wrap')))
        print("Encountered Captcha")
        # driver.switch_to.frame(driver.find_element_by_id("fc-iframe-wrap"))
        print(driver.find_element_by_id("verification-token").get_attribute('value'))
        return [driver.find_element_by_id("verification-token").get_attribute('value'),user,passw]
    except:
        print("Did not encounter a captcha, maybe error finding captcha: ")
        return "Nocaptcha"

    time.sleep(1)

    # try:
    #     driver.execute_script("arguments[0].click();", driver.find_element_by_id("triggerLiteMode"))
    #     print("clicked verify button")
    # except:
    #     print("Did not find verify button: ")




    # try:
    #     WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'CaptchaFrame')))
    #     driver.switch_to.frame(driver.find_element_by_id("CaptchaFrame"))
    # except Exception as e:
    #     print("Did not encounter a captcha, maybe error finding captcha: "+e)

    # time.sleep(1)

    # time.sleep(1)
    #return [driver.find_element_by_id("verification-token").get_attribute('value'),user,passw]

    try:
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, 'navbar-robux')))
        print("Logged in Succesfully with new account...")
    except Exception as e:
        print("Timed out after 40 seconds while signing in with error: "+str(e))


#multithreading bot class that runs the above functions in a loop to generate cookies
class botThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.solver = funcaptchaProxyless()
    def run(self):
        f = open("cookies/cookie_batch_"+randomString()+".txt","w+")
        global stopthreads
        while True:
            if(stopthreads == 1):
                print("Keyboard Interrupted on thread: "+str(self.threadID))
                f.close()
                break
            else:
                driver = initDriver(False)
                signupvals = fillSignUpInfo(driver)
                if(signupvals == "Nocaptcha"):
                    cookie = extractCookie(driver, '.ROBLOSECURITY', 'value')
                elif(signupvals != "Nocaptcha"):
                    try:
                            xsrf_token = ""

                            req = driver.request('POST',
                                url="https://auth.roblox.com/v2/signup",
                                headers={"Origin": "https://www.roblox.com", "Referer": "https://www.roblox.com/account/signupredir", "X-CSRF-TOKEN": xsrf_token, "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"},
                                data={"username":signupvals[1],"password":signupvals[2],"birthday":"01 Jan 2000","gender":"3","isTosAgreementBoxChecked":"true","context":"MultiverseSignupForm","displayAvatarV2":"false","displayContextV2":"false","captchaToken":signupvals[0],"captchaProvider":"PROVIDER_ARKOSE_LABS"}
                            )
                            print(req.text)
                            try:
                                xsrf_token = req.headers["X-CSRF-TOKEN"] # Also here is where i set the XSRF Token as the one returned from url
                                print(xsrf_token)
                            except Exception as e:
                                print("Error: "+str(e))
                            self.solver.set_verbose(1)
                            self.solver.set_key("682169c1074bc756ccc84fd47989d86f")
                            self.solver.set_website_url("https://www.roblox.com/account/signupredir")
                            self.solver.set_website_key("A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F")
                            token = self.solver.solve_and_return_solution()
                            if token != 0:
                                print("result token: "+token)
                            else:
                                print("task finished with error "+self.solver.error_code)
                            # token = input("captcha key: ")
                            signupvals[0] = token

                            headerss={"Origin": "https://www.roblox.com", "Referer": "https://www.roblox.com/account/signupredir", "X-CSRF-TOKEN": xsrf_token, "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36", "Content-Type": "application/json"}
                            resp = driver.request("POST",
                                url="https://auth.roblox.com/v2/signup",
                                headers=headerss,
                                data=json.dumps({"username":signupvals[1],"password":signupvals[2],"birthday":"01 Jan 2000","gender":"3","isTosAgreementBoxChecked":"true","context":"MultiverseSignupForm","displayAvatarV2":"false","displayContextV2":"false","captchaToken":signupvals[0],"captchaProvider":"PROVIDER_ARKOSE_LABS"})
                            )
                            print(signupvals[0])
                            print(resp.text)
                    except Exception as e:
                        print(e)
                #f.write(cookie+"\n")
                driver.quit()
                #time.sleep(15)
                time.sleep(1)
                while True: None

        f.close()



#main loop that starts as many threads as needed
if __name__ == "__main__":
    global stopthreads
    try:
        stopthreads = 0
        bot1 = botThread(1)
        bot1.start()
        # bot2 = botThread(2)
        # bot2.start()
        # bot3 = botThread(3)
        # bot3.start()
        while True:
            None
    except KeyboardInterrupt:
        print('Keyboard Interrupted')
        stopthreads = 1
