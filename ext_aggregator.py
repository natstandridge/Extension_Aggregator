from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import os

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")


driver = webdriver.Chrome('/Users/nat/Library/Application Scripts/chromedriver', options = chrome_options)

#keeps websites from checking if it is a bot or not
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

## clear old files before generating new ones
def prep():
    for i in ['normal_ext.txt','country_ext.txt','country_ext_prepend.txt']:
        try:
            os.remove("extension lists/" + i)
        except:
            pass

## function to add missing periods
def ext_cleaner(input_ext):
    if input_ext[0] != ".":
        return("." + input_ext)
    else:
        return(input_ext)

## First two sets are 'normal' top-level domains
output_normal_list = []
def get_normal_set():
    driver.get('https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains')
    global output_normal_list
    ## starting row/table values
    row = 1
    table = 2

    rows = driver.find_elements_by_xpath(f"//*[@id='mw-content-text']/div[1]/table[{table}]/tbody/tr")
    row_count = len(rows)
    tables = driver.find_elements_by_xpath("//*[@id='mw-content-text']/div[1]/table")
    table_count = len(tables)

    ## This has to stop at 30 to avoid some empty tables in between this and table 42
    while table < 30:
        while row:
            try:
                with open('extension lists/normal_ext.txt', 'a') as f:
                    extension = driver.find_element_by_xpath(f"//*[@id='mw-content-text']/div[1]/table[{table}]/tbody/tr[{row}]/td[1]/a").text
                    extension = str(extension)

                    extension = ext_cleaner(extension)

                    print(extension)
                    if len(extension) > 1:
                        f.write(extension + "\n")
                        output_normal_list.append(extension)
                        row += 1
                        if row >= row_count:
                            break
                        else:
                            pass
                    else:
                        break
            except:
                #print("In exception for with open")
                row = 1
                table += 1
                pass
    
    f.close

    ## reset variables to skip blank sections and move to second set
    row = 1
    table = 42
    rows = driver.find_elements_by_xpath(f"//*[@id='mw-content-text']/div[1]/table[{table}]/tbody/tr")
    row_count = len(rows)
    tables = driver.find_elements_by_xpath("//*[@id='mw-content-text']/div[1]/table")
    table_count = len(tables)

    while table <= table_count:
        while row:
            try:
                with open('extension lists/normal_ext.txt', 'a') as f:
                    
                    extension = driver.find_element_by_xpath(f"//*[@id='mw-content-text']/div[1]/table[{table}]/tbody/tr[{row}]/td[1]/a").text
                    extension = str(extension)

                    extension = ext_cleaner(extension)

                    print(extension)

                    if len(extension) > 1:
                        f.write(extension + "\n")
                        output_country_list.append(extension)
                        row += 1
                        if row >= row_count:
                            break
                        else:
                            pass
                    else:
                        break

            except:
                row = 1
                table += 1
                if table >= table_count:
                    break
                pass

    return(output_normal_list)
    f.close()

output_country_list = []
def get_country_set():
    global output_country_list
    driver.get('https://en.wikipedia.org/wiki/Country_code_top-level_domain')
    
    row = 1
    table = 1
    rows = driver.find_elements_by_xpath(f"//*[@id='mw-content-text']/div[1]/table[{table}]/tbody/tr")
    row_count = len(rows)
    tables = driver.find_elements_by_xpath("//*[@id='mw-content-text']/div[1]/table")
    table_count = len(tables)
    print(len(tables))

    output_country_list = []
    while table <= table_count:
        print(f"Table count is : {table}")
        while row:
            try:
                with open('extension lists/country_ext.txt', 'a') as f:
            
                    extension = driver.find_element_by_xpath(f"//*[@id='mw-content-text']/div[1]/table[{table}]/tbody/tr[{row}]/td[1]/a").text
                    extension = str(extension)

                    extension = ext_cleaner(extension)

                    print(extension)

                    if len(extension) > 1:
                        f.write(extension + "\n")
                        output_country_list.append(extension)
                        row += 1
                        if row >= row_count:
                            break
                        else:
                            pass
                    else:
                        break

            except:
                row = 1
                table += 1
                if table >= table_count:
                    break
                pass
    return(output_country_list)
    f.close()

## creates an alternate list for prepending country code instead of appending
output_country_prepend_list = []
def make_country_prepend_list():
    global output_country_list, output_country_prepend_list

    count = 0
    for i in output_country_list:
        if i[0] == '.':
            output_country_list[count] = i[1:] + '.'
            with open('extension lists/country_ext_prepend.txt', 'a') as f:
                f.write(output_country_list[count] + '\n')
                print(output_country_list[count])
                output_country_prepend_list.append(output_country_list[count])
        else:
            pass
    f.close()

def main():
    prep()
    print("Starting normal set.")
    get_normal_set()
    print("Starting country set.")
    get_country_set()
    print("Creating country prepend list.")
    make_country_prepend_list()

if __name__ == "__main__":
    main()