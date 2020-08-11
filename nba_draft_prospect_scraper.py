#import requests
import lxml.html as lh
import pandas as pd
from selenium import webdriver
from urllib.request import Request, urlopen
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import re
import time

url='https://www.nba.com/draft/2020/prospects#/'

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get(url)
time.sleep(5) # wait to load

# now print the response
print(type(driver.page_source))

doc = lh.fromstring(driver.page_source)
driver.close()
tr_elements = doc.xpath('//tr')
tr_elements = tr_elements[1:]

# Remove unnecessary columns
for el in tr_elements:
    del el[1], el[5]

# Names are scraped as Last,FirstF. Last
# Change to Last, First
name_list = []
for el in tr_elements:
    full_str = el[0].text_content()
    name_list_case = re.findall('[A-Z][^A-Z]*', full_str)
    #print(name_list_case)
    name_list.append(name_list_case[0] + name_list_case[1])

# Fill dictionary with data
data_dict = { 'Name': name_list }
for i in range(1, 6):
    name = tr_elements[0][i].text_content().split()[0] # Manipulate string to get column names
    info = [el[i].text_content().split()[1] for el in tr_elements]
    data_dict[name] = info

df = pd.DataFrame.from_dict(data_dict)
print(df.head())
