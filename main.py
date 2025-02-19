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

# import argparse for con
# output in run-time
#
def check_connect_sub(driver):
    driver.refresh()
    time.sleep(10)
    try:
        error = driver.find_element(By.ID, "main-frame-error")
        return True
    except Exception as e:
        return False




def checking_internet_connection(driver):
    # Checking internet is error or not.
    try:
        alert_icon = driver.find_element(By.CLASS_NAME, 'apollo-icon-alert-circle')
        # Wait for the network connection connected again. Check the connection every 2 seconds.
        while check_connect_sub(driver):
            print("Internet is interrupted")
        return True
    except Exception as e:
        return True


def extract_page(data_url, rows_number, driver,add_linkedin):
    info_list = list()
    driver.get(data_url)
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.XPATH, '//div[contains(@role,"treegrid")]')))
    time.sleep(10)

    if (checking_internet_connection(driver)):
        # Add linkedin as requirement.
        if add_linkedin == True:
            driver.find_element(By.CLASS_NAME,'apollo-icon-plus').click()
            ActionChains(driver) \
                .send_keys("Links") \
                .send_keys(Keys.ENTER) \
                .perform()
            ActionBuilder(driver).clear_actions()
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        time.sleep(3)

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

            # email-5
            try:
                email_button = rows[i].find_element(By.CLASS_NAME, "apollo-colored-icon")
                parrent_email = email_button.find_element(By.XPATH,"./..")
                # ActionChains(driver) \
                #     .move_to_element(parrent_email) \
                #     .click() \
                #     .perform()
                # ActionBuilder(driver).clear_actions()
                driver.execute_script("arguments[0].click();", parrent_email)
                # time.sleep(2)
                email = driver.find_element(By.XPATH, '//div[@data-testid="ContactInformationContainer"]')
                sub_list.append(email.text.split("\n")[0])
            except selenium.common.exceptions.NoSuchElementException as e:
                sub_list.append("N/A")

            # Add linkedin
            linkedin = rows[i].find_element(By.CLASS_NAME, 'apollo-icon-linkedin')
            parrent = linkedin.find_element(By.XPATH, "./..")
            sub_list.append(parrent.get_attribute("href"))

            # Status
            sub_list.append("")

            sub_list.append(sub[5])
            sub_list.append(sub[6])
            if sub[1].__contains__("Update available"):
                print("break")
                sub_list[1] = sub[2]
                sub_list[2] = sub[4]
                sub_list[6] = sub[8]
                sub_list[7] = sub[9]
            # phone-6
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            phone_button =  rows[i].find_element(By.CLASS_NAME, "apollo-icon-phone")
            parrent_phone = phone_button.find_element(By.XPATH, "./..")
            try:
                # ActionChains(driver) \
                #     .move_to_element(parrent_phone) \
                #     .click() \
                #     .perform()
                # ActionBuilder(driver).clear_actions()
                driver.execute_script("arguments[0].click();", parrent_phone)
                # time.sleep(2)
                phone_number = driver.find_element(By.XPATH, '//div[@data-testid="ContactPhoneInformationContainer"]')
                phone_number.find_element(By.TAG_NAME, 'label').click()
                sub_list.append(phone_number.text.split("\n")[1])
            except Exception as e:
                sub_list.append("N/A")
                sub_list[6] = sub[4]
                sub_list[7] = sub[5]
            #     Remove company keywords.
            # sub_list.append(rows[i].text.split(sub_list[4])[1].strip("\n"))
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            info_list.append(sub_list)
    return info_list




## Create a session objec
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web scraping")
    parser.add_argument("-min", help="min time you want", required=True)
    parser.add_argument("-max", help="max time you want to wait", required=True)
    parser.add_argument("-output", help="output file name, e.x myfile.csv", required=True)
    parser.add_argument("-url", help="URL of first page you want to scrape, all the next page will be calculated", required=True)
    parser.add_argument("-records", help="Total records contain in that webpage", required=True)

    args = parser.parse_args()
    start_time = time.time()
    # calculate total number
    total_number = int(args.records)
    rows_number = 25
    my_array = list()
    for i in range(1, total_number // rows_number + 1):
        my_array.append(25)
    if total_number % rows_number != 0:
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
        if count == 0:
            flag = True
        else:
            flag = False
        info_list = extract_page(data_url=data_url,rows_number=rows_number,driver=driver, add_linkedin=flag)
        time.sleep(time_random)
        final_list = final_list + info_list
        count = count + 1
        if count < my_array.__len__():
            go_to_next = driver.find_element(By.CLASS_NAME, 'apollo-icon-chevron-arrow-right')
            driver.execute_script("arguments[0].click();", go_to_next)
            time.sleep(1)
            data_url = driver.current_url



    driver.close()
    pandas.DataFrame(final_list, columns=['Name','Job Title', 'Company','Email', 'URL Linkedin', 'Status','Location', 'Company Number','Phone']).to_csv(f"{args.output}",index=False)
    print(f"Time taken: {time.time() - start_time}\n")


    print("Output file here: \n")
    print(os.path.join(os.getcwd(),args.output))



