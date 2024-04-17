from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from plyer import notification
import time

url = "https://apps3.alameda.courts.ca.gov/webpay/views/citation-entry.aspx"
id_lastname= "ctl00_ContentPlaceholder1_txtLastName"
id_dob="ctl00_ContentPlaceholder1_txtDOB"
id_submit="ctl00_ContentPlaceholder1_btnSubmitName"
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get(url)

    with open(r'C:\Users\hanji\Desktop\Citation Check\inputs.txt','r') as file:
        lastname = file.readline()
        dob = file.readline()
    input_lastname = driver.find_element(By.ID,id_lastname)
    input_lastname.send_keys(lastname)
    input_dob = driver.find_element(By.ID,id_dob)
    input_dob.send_keys(dob)

    data = ""

    #driver.find_element(By.ID,id_submit).click()

    submit_button = driver.find_element(By.ID,id_submit)
    ActionChains(driver).move_to_element(submit_button).perform()
    time.sleep(1)  # Adjust the wait time as needed

    # Click on the submit button using JavaScript
    driver.execute_script("arguments[0].click();", submit_button)

    rows = len(driver.find_elements(By.XPATH,'//*[@id="ctl00_ContentPlaceholder1_gvCitations"]/tbody/tr'))
    cols = len(driver.find_elements(By.XPATH,'//*[@id="ctl00_ContentPlaceholder1_gvCitations"]/tbody/tr[1]/td'))
    for i in range(2,rows+1):
        for j in range(2,cols+1):
            xpath = '//*[@id="ctl00_ContentPlaceholder1_gvCitations"]/tbody/tr[{}]/td[{}]'.format(i, j)
            value = driver.find_element(By.XPATH,xpath).text
            data += value + " "
        data += '\n'

    with open(r'C:\Users\hanji\Desktop\Citation Check\citations.txt','r') as file:
        currData = file.read()

    if data != currData:
        notification.notify(
            title = "New Citations Found",
            message = "Please check the citation website for more detail",
            app_name = "Citation Check",
            timeout = 10
        )
        with open(r'C:\Users\hanji\Desktop\Citation Check\citations.txt','w') as file:
            file.write(data)
finally:
    driver.close()