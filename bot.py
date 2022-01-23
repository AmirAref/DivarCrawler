#Programmer : t.me/Amir_720
# import
from selenium import webdriver
from Divar_Scraper_Pro import login_divar, get_phone_numbers, divar_serach_sl
from time import ctime,sleep
from datetime import datetime
import os,json

from config import *
# -----functions ----------

#json get cities
def Get_cities():
    return json.load(open("Cities.json","r"))


# get str time format
def time_format():
    now = datetime.now()
    strTime = datetime.strftime(now, "%Y-%m-%d_%H-%M-%S")

    return strTime

# create path
def create_path(path):
    if not os.path.exists(path):
        os.mkdir(path)


# save new file
def save_new_file(path, file_name, data):
    # create path
    create_path(path)

    # convert data to string data
    data = filter(lambda x:not(not x), data)
    data = map(str, data)
    data = "\n".join(data)

    # create file
    with open(path + "/" + file_name, "w", encoding="utf-8") as file:
        file.write(data)

    
# update file
def update_file(path, file_name, new_data):
    # create path
    create_path(path)
    
    old_data = []

    # read old file
    try:
        with open(path + "/" + file_name, "r", encoding="utf-8") as file:
            old_data = file.read().split('\n')
    except :
        old_data = []

    # all data
    all_data = new_data + old_data
    all_data = tuple(set(all_data))

    # save new data + old data
    save_new_file(path, file_name, all_data)




# extraction process
def Extraction_Process(output_path, driver, query, limit, city='tehran', category=None):
    # fields
    phones = []
    urls = []

    # extract urls
    urls = divar_serach_sl(driver, query, city, category, limit)
    if not urls:
        print("Error to Extract Urls !")
        return False

    # extract phone numbers
    phones = get_phone_numbers(driver, urls)
    if not phones:
        print("Phones is empty !")
        return False

    # clear cache

    # save new result
    file_name = f"{query}-{city}-{time_format()}.txt"
    save_new_file(output_path + "/log", file_name, phones)

    # update old result
    file_name = f"{query}-{city}.txt"
    update_file(output_path, file_name, phones)


# one time extract
def main():
    # create output path
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    # start driver
    driver = webdriver.Edge('msedgedriver.exe')
    driver.maximize_window()

    # login divar.ir
    login_divar(driver, phone)

    # firstly extractin process
    Extraction_Process(output_path=output_path, driver=driver,
                                query=query, limit=limit, city=city, category=category)
    
    
    '''
    #run loop
    while(True):
        try:
            #do function
            Extraction_Process(output_path=output_path, driver=driver,
                                query=query, limit=100, city=city, category=category)
            #sleeping
            sleep(time_loop_check)
        except Exception as e:
            print(e)
            pass
    '''

    # close driver
    driver.close()


# -----------------------------
if __name__ == "__main__":
    main()
    input("Press Any key to quit !")
