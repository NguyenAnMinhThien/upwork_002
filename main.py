import time
import os
import random
from selenium.webdriver.common.actions.action_builder import ActionBuilder
import pandas
import re
import selenium
from selenium.webdriver import Keys, ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse

def extract_page(data_url, rows_number, driver):
    info_list = list()
    driver.get(data_url)
    WebDriverWait(driver,10).until(expected_conditions.presence_of_element_located((By.XPATH, '//div[contains(@role,"treegrid")]')))
    time.sleep(10)

    treegrid = driver.find_element(By.XPATH, '//div[contains(@role,"treegrid")]')
    rows = treegrid.find_elements(By.XPATH, '//div[contains(@role,"row")]')
    if rows.__len__() < 1:
        print("Your URl is wrong, please input again.")
    for i in range(3, rows_number + 3):
        sub_list = list()
        sub = rows[i].text.split("\n")
        sub_list.append(sub[0])
        sub_list.append(sub[1])
        sub_list.append(sub[2])
        sub_list.append(sub[5])
        sub_list.append(sub[6])
        if sub[1].__contains__("Update available"):
            print("break")
            sub_list[1] = sub[2]
            sub_list[2] = sub[4]
            sub_list[3] = sub[8]
            sub_list[4] = sub[9]
        # email-5
        try:
            email_button = rows[i].find_element(By.CLASS_NAME, "apollo-colored-icon")
            ActionChains(driver) \
                .move_to_element(email_button) \
                .click() \
                .perform()
            ActionBuilder(driver).clear_actions()
            # time.sleep(2)
            email = driver.find_element(By.XPATH, '//div[@data-testid="ContactInformationContainer"]')
            sub_list.append(email.text.split("\n")[0])
        except selenium.common.exceptions.NoSuchElementException as e:
            sub_list.append("N/A")

        # phone-6
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        phone_button =  rows[i].find_element(By.CLASS_NAME, "apollo-icon-phone")
        try:
            ActionChains(driver) \
                .move_to_element(phone_button) \
                .click() \
                .perform()
            ActionBuilder(driver).clear_actions()
            # time.sleep(2)
            phone_number = driver.find_element(By.XPATH, '//div[@data-testid="ContactPhoneInformationContainer"]')
            phone_number.find_element(By.TAG_NAME, 'label').click()
            sub_list.append(phone_number.text.split("\n")[1])
        except Exception as e:
            sub_list.append("N/A")
        sub_list.append(rows[i].text.split(sub_list[4])[1].strip("\n"))
        info_list.append(sub_list)
    return info_list

def move_next_range(driver, select):
    ActionChains(driver) \
        .move_to_element(select) \
        .click_and_hold() \
        .key_down(Keys.ARROW_DOWN) \
        .key_down(Keys.ENTER) \
        .pause(2) \
        .perform()
    ActionBuilder(driver).clear_actions()
## Create a session objec
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web scraping")
    parser.add_argument("-min", help="min time you want", required=True)
    parser.add_argument("-max", help="max time you want to wait", required=True)
    parser.add_argument("-output", help="output file name, e.x myfile.csv", required=True)
    parser.add_argument("-url", help="URL of first page you want to scrape, all the next page will be calculated", required=True)
    parser.add_argument("-records", help="Total records contain in that webpage", required=True)

    args = parser.parse_args()
    # calculate total number
    total_number = int(args.records)
    rows_number = 25
    my_array = list()
    for i in range(1, total_number // rows_number + 1):
        my_array.append(25)
    my_array.append(total_number % rows_number)

    # time waiting between extract page
    time_random = random.randint(int(args.min),int(args.max) + 1)


    driver = webdriver.Chrome()
    driver.get("https://app.apollo.io/#/login")
    WebDriverWait(driver,10).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[contains(@data-cy,"login-button")]')))
    time.sleep(5)
    info_list = list()
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    inputs[0].send_keys("marcus@aiworkerz.com")
    inputs[1].send_keys("j;*v'&sH8.#RLc3")
    driver.find_element(By.XPATH, '//*[contains(@data-cy,"login-button")]').click()
    time.sleep(10)
    data_url = args.url

    final_list = list()
    count = 0
    for rows_number in my_array:
        info_list = extract_page(data_url=data_url,rows_number=rows_number,driver=driver)
        time.sleep(time_random)
        final_list = final_list + info_list
        count = count + 1
        if count < my_array.__len__():
            driver.find_element(By.CLASS_NAME, 'apollo-icon-chevron-arrow-right').click()

    driver.close()
    pandas.DataFrame(final_list, columns=['Name','Job Title', 'Company','Location', 'Company','Email','Phone','Company industries and Keywords']).to_csv(f"{args.output}",index=False)


    print("Output file here: \n")
    print(os.path.join(os.getcwd(),args.output))



