from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re 
import os
import string
cwd = os.getcwd()

opts = Options()
opts.headless = True
opts.add_argument('log-level=3') 
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option('excludeSwitches', ['enable-logging'])
path_browser = f"{cwd}\chromedriver.exe"

 
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters + string.digits) for i in range(length))
    return result_str

def manage_account():
    # try:
    
    wait(browser,30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="viewport"]/div[5]/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div/div[2]/div[1]/div'))).click()
    print(f"[*] [ {email} ] Success Login")
    print(f"[*] [ {email} ] Trying to Change Username")
    sleep(1)
    wait(browser,30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div/div/div[3]/div/div[3]/div/div[2]/div/div/div/div[1]/div/div[1]/div/div[3]/div/div/button'))).click()

    sleep(1)
    wait(browser,30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/div[2]/div[2]/div/button'))).click()
    username = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/div[2]/div/div/div[1]/div/div/input')))
    try:
        username.send_keys(Keys.CONTROL + "a")
        username.send_keys(Keys.DELETE)
    except:
        pass

    username.send_keys(f"{get_random_string(5)}{random.randint(10,99)}{get_random_string(35)}")
    wait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/div[2]/div/div/button"))).click()
    try:
        username_new = wait(browser,25).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div/div/div/div[2]/div[3]/div/div[3]/div[2]/div[2]/div[1]"))).text
        print(f"[*] [ {email} ] Username Change to [ {username_new} ]")
        wait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div/div/div[2]/div[3]/div[3]/div/div/button"))).click()
        get_notif = wait(browser,45).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div/div/div/div[2]/div[3]/div[2]/div[2]/div[1]/div/div/div[2]/span/span"))).text
        print(f"[*] [ {email} ] Status: {get_notif}")
        
        with open('success.txt','a') as f:
            f.write('{0}|{1}\n'.format(username_new,password))
        browser.quit()
    except:
        print(f"[*] [ {email} ] Failed Change Username!")
        with open('failed.txt','a') as f:
            f.write('{0}|{1}\n'.format(email,password))
        browser.quit()
    # except: 
    #     print(f"[*] [ {email} ] Failed First Stage!") 
    #     with open('failed_first.txt','a') as f:
    #             f.write('{0}|{1}\n'.format(email,password))       
    
def open_browser(k):
    
    global browser
    global element
    global password
    global email
    k = k.split("|")
    email = k[0]
    password = k[1]
    random_angka = random.randint(100,999)
    random_angka_dua = random.randint(10,99)
    opts.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.{random_angka}.{random_angka_dua} Safari/537.36")
    browser = webdriver.Chrome(options=opts, desired_capabilities=dc, executable_path=path_browser)
    browser.get('https://admin.microsoft.com/Adminportal/Home?source=applauncher#/users')

    print(f"[*] [ {email} ] Trying to Login")
    element = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]")))
    element.send_keys(email)
        
    sleep(0.5)
    element.send_keys(Keys.ENTER) 
    element = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[2]/div/div[2]/input")))
    element.send_keys(password)
        
    sleep(0.5)
    element.send_keys(Keys.ENTER) 
    try:
        wait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/form/div/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input"))).click()

    except:
        pass
    manage_account()

if __name__ == '__main__':
    global list_accountsplit
    global k
    print("[*] Automation Change Username Microsoft")
    print("[*] Format: email|password")
    jumlah = int(input("[*] Multi Processing: "))
    file_list = "admin.txt"
    myfile = open(f"{cwd}/{file_list}","r")
    list_account = myfile.read()
    list_accountsplit = list_account.split()
    k = list_accountsplit
    with Pool(jumlah) as p:  
        p.map(open_browser, k)

    print("[*] Automation Finish!")
