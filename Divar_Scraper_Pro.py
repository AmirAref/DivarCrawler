#Programmer : t.me/Amir_720
#import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
import os,pickle,requests
#-------------------------values---------------------------------------
cookies_path = "phones"
is_Ban_Account = False


#create cookies path
if not os.path.exists(cookies_path):
    os.mkdir(cookies_path)
#---------------------------functions-------------------------------------
def get_cookies(phone):
    cookies = pickle.load(open(f"{cookies_path}/{phone}.pkl", "rb"))
    return cookies

#save cookies
def save_cookies(cookies, phone):
    pickle.dump( cookies , open(f"{cookies_path}/{phone}.pkl","wb"))

#exist seesion cookies
def exist_session(phone):
    return os.path.exists(f"{cookies_path}/{phone}.pkl")

#add cokkies
def add_cookies(driver, cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)

#login in the divar.ir
def login_divar(driver, phone):
    #have error function
    def is_error():
        try:
            driver.find_element_by_class_name("form-error")
            return True
        except:
            return False
    
    #driver get
    driver.get("https://divar.ir")
    sleep(2)


    '''
    #load cookies
    if exist_session(phone):
        cookies = get_cookies(phone)
        add_cookies(driver, cookies)
    '''
        
    try:
        #find login 2 button
        sleep(1)
        login_1 = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/button')
        login_1.click()
        #find login 2 button
        sleep(1)
        login_2 = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/div/div/button')
        login_2.click()
        #find and send phone to input
        sleep(1)
        phone_input = driver.find_element_by_name("mobile")
        phone_input.send_keys(phone)
        #find login 3 button
        sleep(1)
        login_3 = driver.find_element_by_xpath('/html/body/div[2]/div/article/div/footer/div/button')
        login_3.click()
        #check have error message
        if is_error():
            return False
        
        #find and send code to input
        sleep(1)
        code = input("Enter code from your messages : ")
        phone_input = driver.find_element_by_name("code")
        phone_input.send_keys(code)
        #find login 4 button
        '''
        sleep(1)
        login_4 = driver.find_element_by_xpath('/html/body/div[2]/div/article/div/footer/div/button[2]')
        login_4.click()
        '''
    except Exception as e:
        print(e)
        return False

    #save cookies
    #save_cookies(driver.get_cookies(), phone)

    sleep(2)
    return True



def is_Phone_Ban(driver):
    
    _par_text = "محدودیت نمایش اطلاعات تماس"

    return _par_text in driver.page_source


#get phone number from page
def get_phone_number(driver, url, agree=False):
    global is_Ban_Account

    #click on agree button
    def click_agree():
        sleep(1)
        
        try:
            #agree = driver.find_element_by_class_name("kt-button--primary")
            #/html/body/div[2]/div/article/div/footer/button
            agree = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/article/div/footer/button"))
            )
            agree.click()
            print("******************************clicked agree")
        except Exception as e:
            #print("******************************clicked agree erorr")
            #print(e)
            return
    #load page
    driver.get(url)
    sleep(2)
    #find contacts button
    try:
        button_contacts = driver.find_element_by_class_name("post-actions__get-contact")
    except:
        return
    #clieck on the button 
    button_contacts.click()

    #click i agree
    if agree:
        click_agree()

    #sleep
    sleep(2)


    #check is ban or no
    if(is_Phone_Ban(driver)):
        is_Ban_Account = True
        return


    try:
        #get number
        #//*[@id="app"]/div[2]/div/div[1]/div/div[3]/div[1]/div/div[2]/a
        phone = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[1]/div/div[3]/div[1]/div/div[2]/a')
        phone = numeric_fa_to_en(phone.text)
        if not phone.isdigit():
            return 
        return phone
    except Exception as e:
        #print(e)
        return


#convert persian numbers to english numbers
def numeric_fa_to_en(text):
    fa = "۰۱۲۳۴۵۶۷۸۹"
    en = "0123456789"
    n = len(fa)

    for i in range(n):
        item1 = fa[i]
        item2 = en[i]
        if item1 in text:
            text = text.replace(item1, item2)
    return text


#get phone numbers from urls
def get_phone_numbers(driver, urls):
    #fileds
    phones = []
    first = True

    #extract phone numbers
    for url in urls:
        if first:
            first = False
            agree = True
        else:
            agree = False
        #check ban account
        if is_Ban_Account:
            print("Account Banned !")
            break
        try:
            phone = get_phone_number(driver, url, agree=agree)
        except Exception as e:
            #print(e)
            continue
        #
        if not phone:
            continue
        #add
        phone = numeric_fa_to_en(phone)
        phones.append(phone)
    
    return phones


#extract urls function
def extract_urls(page_source):
    #set url function
    def get_url(soup, base_url='https://divar.ir'):
        a = soup.find('a')['href']
        if a.startswith('/'):
            a = base_url + a
        return a
    #bs4
    soup = BeautifulSoup(page_source, 'html.parser')
    #find all items
    result = soup.find_all('div', attrs={'class': 'post-card-item'})[1:-1]
    #set urls
    result = list(map(get_url, result))
    #out
    return result

#check validition url
def ValiditionUrl(url):
    try:
       requests.get(url)
       return True
    except Exception as e:
        return False


#change city click agree
def change_city(driver):
    sleep(1)
    try:
        #kt-button kt-button--primary multi-city-change-alert-actions
        #agree = driver.find_element_by_class_name('multi-city-change-alert-actions')
        agree = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "multi-city-change-alert-actions"))
        )
        agree.click()
        print("******************************clicked change city agree")
        return True
    except Exception as e:
        print("******************************clicked change city agree erorr")
        #print(e)
        return False


#extract links from divar.ir
def divar_serach_sl(driver, query, city='tehran', catigory=None, limit = None):

    if catigory:
        url = f'https://divar.ir/s/{city}/{catigory}?q={query}'
    else:
        url = f'https://divar.ir/s/{city}?q={query}'
    #validition url
    if not ValiditionUrl(url):
        return
    
    #get
    driver.get(url)
        
    #fileds
    result = []
    #------------Scrolling-------------
    SCROLL_PAUSE_TIME = 0.8

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    b = 0

    while True:#b < 100:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #add new result
        result.extend(extract_urls(driver.page_source))

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        #check limit
        if limit and len(result) > limit:
            break
        #
        last_height = new_height
        b += 1
    #-------------------------
    #optimizing result
    result = list(set(result))
    #set limit
    if limit:
        result = result[:limit]

    return result