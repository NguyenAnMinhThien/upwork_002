import time

import requests
from bs4 import BeautifulSoup

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

## Create a session object
driver = webdriver.Chrome()
session = requests.Session()

headers = {
    'accept': '*/*',
    'accept-language': 'en,en-US;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://app.apollo.io',
    'priority': 'u=1, i',
    'referer': 'https://app.apollo.io/',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
}

data = {
    'checksum': 'be6ccf6f907a490da743687b45d92e18',
    'client': '122a93c7d9753d2fe678deffe8fac4cf',
    'e': '[{"device_id":"4188df88-96fd-4dba-8c02-204acb822928R","user_id":"6510f144dbb7cc00a30c4a98","timestamp":1739781530748,"event_id":46,"session_id":1739772915481,"event_type":"Login Page CTA Clicked","version_name":null,"platform":"Web","os_name":"Chrome","os_version":"133","device_model":"Windows","device_manufacturer":null,"language":"en","carrier":null,"api_properties":{},"event_properties":{"type":"Login","mode":"Login with Email"},"user_properties":{},"uuid":"871844a2-ace3-45ba-9007-58c53abac68f","library":{"name":"amplitude-js","version":"5.8.0"},"sequence_number":111,"groups":{},"group_properties":{},"user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}]',
    'upload_time': '1739781530749',
    'v': '2',
}


response = session.post('https://www.apollo.io/amp-outbound/', headers=headers, data=data)
# ## Add our login data
# login_url = 'https://api-iam.intercom.io/messenger/web/launcher_settings'
# credentials = {
#     'email': 'marcus@aiworkerz.com',
#     'password': 'j;*v'+'&sH8.#RLc3'
# }
# print(credentials['password'])
# ## Send a POST request to our endpoint
# response = session.post(login_url, data=credentials)
print(response)
if response.ok:
    print("Login successful!")
else:
    print("Login failed!")

data_url = 'https://app.apollo.io/#/people?page=1&contactLabelIds[]=67aec75ef29f220015040582&prospectedByCurrentTeam[]=yes&sortByField=%5Bnone%5D&sortAscending=false'
data_page = session.get(data_url, headers=headers, data=data)
time.sleep(5)

if data_page.ok:
    print("Data retrieved successfully!")

    # Use Beautiful Soup to parse HTML content
    soup = BeautifulSoup(data_page.text, 'html.parser')

    print(data_page.text)
    # Example of finding an element by tag
    # first_paragraph = soup.find('h1')
    # print("First text:", first_paragraph.text)

else:
    print("Failed to retrieve data.")