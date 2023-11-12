# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
driver.get("https://www.apartments.com/")

title = driver.title

# sign in
SIGNIN = (By.XPATH, '//*[@id="headerLoginSection"]/a[3]')
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(SIGNIN)).click()


LOGINMODAL = (By.ID, 'loginContainer')
LOGINMODAL_ELEMENT = driver.find_element(By.ID, 'loginContainer')
WebDriverWait(driver, 10).until(EC.visibility_of_element_located(LOGINMODAL))

# driver.implicitly_wait(100)

iframe = driver.find_element(By.XPATH, '//*[@id="iFrameResizer0"]')
driver.switch_to.frame(iframe)

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="username"]')))

USERNAME = driver.find_element(By.XPATH, '//*[@id="username"]')
# PASSWORD = (By.XPATH, '//*[@id="password"]')

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
PASSWORD = driver.find_element(By.XPATH, '//*[@id="password"]')
# SUBMITBOTTON = (By.XPATH, '//*[@id="loginButton"]')
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="loginButton"]')))
SUBMITBOTTON = driver.find_element(By.XPATH, '//*[@id="loginButton"]')


USERNAME.send_keys("171250011xyd@gmail.com")

PASSWORD.send_keys("vgS!Q49TG+QfqDk")

SUBMITBOTTON.click()

# print(title)

#back to the main frame to continue the script
driver.switch_to.default_content()

# WebDriverWait(driver, 10).until(LOGINMODAL_ELEMENT.())
# click search
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="quickSearch"]/div/div/a')) )
time.sleep(8)
SEARCHBUTTON = driver.find_element(By.XPATH, '//*[@id="quickSearch"]/div/div/a')
SEARCHBUTTON.click()
nextPage = [6,7,7,7,7,8,9,9,9,9,9,9,9,9,9,9,9,9,9,9]
# crawl the data
data = []
for i in range(16):
# for i in range(1):
    time.sleep(4)
    for j in range(25):
        # each_item = driver.find_element(By.XPATH, '//*[@id="placardContainer"]/ul'+'/li['+str(j+1)+']')
        apartment_name = driver.find_element(By.XPATH, '// *[ @ id = "placardContainer"] / ul / li['+str(j+1)+'] / article / header / div[1] / a / div[1] / span').text
        address = driver.find_element(By.XPATH, '// *[ @ id = "placardContainer"] / ul / li['+str(j+1)+'] / article / header / div[1] / a / div[2]').text
        # address_split = address.split(", ")
        # street = address_split[0]
        # city = address_split[1]

        price = driver.find_element(By.XPATH, '// *[ @ id = "placardContainer"] / ul / li['+str(j+1)+'] / article / section / div / div[2] / div / div[1] / a / p[1]').text
        #// *[ @ id = "placardContainer"] / ul / li[1] / article / section / div / div[2] / div / div[1] / a / p[1]
        lowerPrice = 0
        higherPrice = 0
        if len(price) != 0 and price[0] == '$':
            price_range = price[1:].split(' - ')
            if(len(price_range) > 1):
                lowerPrice = price_range[0]
                higherPrice = price_range[1]
            else:
                lowerPrice = price_range[0]
                higherPrice = price_range[0]
        beds_property = driver.find_element(By.XPATH, '// *[ @ id = "placardContainer"] / ul / li['+str(j+1)+'] / article / section / div / div[2] / div / div[1] / a / p[2]').text
        phone_num = driver.find_element(By.XPATH, '// *[ @ id = "placardContainer"] / ul / li['+str(j+1)+'] / article / section / div / div[2] / div / div[2] / a / span').text

        curr_li = driver.find_element(By.XPATH, '//*[@id="placardContainer"]/ul/li['+str(j+1)+']')
        property_link = curr_li.find_element(By.CLASS_NAME,"property-amenities")
        options = property_link.find_elements(By.TAG_NAME,"span")

        property_list = []
        for option in options:
            if len(option.text) != 0:
                property_list.append(option.text)

        # special = []
        #
        # // *[ @ id = "placardContainer"] / ul / li[1] / article / section / div / div[2] / div / a / p / span[1]


        json_bean = dict()
        json_bean['apartment_name'] = apartment_name
        json_bean['address'] = address
        json_bean['lowerPrice'] = lowerPrice
        json_bean['higherPrice'] = higherPrice
        json_bean['beds_property'] = beds_property
        json_bean['phone_num'] = phone_num
        json_bean['property'] = property_list
        # Serializing json
        data.append(json_bean)
        # json.dumps(json_bean, outfile, ensure_ascii=False, indent=6)
        print(apartment_name)
        print(address)
    # move to next page
    # next page
    change_page = driver.find_element(By.XPATH, '//*[@id="paging"]/ol/li['+str(nextPage[i])+']/a').click()

with open("sample.json", "w") as outfile:
    json_data = json.dumps(data, ensure_ascii=False, indent=7)
    outfile.write(json_data)
# SCRIPTDATA = driver.find_element(By.XPATH, '//*[@id="placardContainer"]/ul')
# print(SCRIPTDATA)
# # script_string = SCRIPTDATA.get_attribute("innerHTML")
# # script_dict = json.loads(script_string)
# # print(script_dict)
#
# #print([my_elem.text for my_elem in driver.find_element(By.XPATH, '//*[@id="placardContainer"]/ul')])
# //*[@id="placardContainer"]/ul/li[1]