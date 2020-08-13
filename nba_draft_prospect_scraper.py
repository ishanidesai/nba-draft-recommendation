import lxml.html as lh
import pandas as pd
from selenium import webdriver
from urllib.request import Request, urlopen
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import itertools as it
import re
import time

#url='https://www.nba.com/draft/2020/prospects#/'

# Names are scraped as Last,FirstF. Last...Change format to First Last
def string_manipulate_name(full_str):
    divided_str = full_str.split()
    middle_str = ''
    for str in divided_str:
        if (sum(1 for c in str if c.isupper()) >= 2) and ('.' in str):
            middle_str = str
    delimiter = middle_str[-2:]
    first_name = middle_str[:-2]
    last_name = full_str.split(delimiter + ' ')[-1]
    print(first_name + ' ' + last_name)
    return first_name + ' ' + last_name


def scrape_nba_draft_prospects(url):

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
        print(el[0].text_content())
        del el[1]#, el[5]

    # Dictionary for prospect info
    data_dict = {}

    # Add 'Name' to dictionary
    names = []
    for el in tr_elements:
        names.append(string_manipulate_name(el[0].text_content()))
    data_dict['Name'] = names

    # Add 'Status' to dictionary
    if 'Status' in tr_elements[0][5].text_content():
        col_info = [el[5].text_content().replace('Status', '') for el in tr_elements]
        data_dict['Status'] = col_info

    for i in it.chain(range(1, 5), range(6,7)):
        name = tr_elements[0][i].text_content().split()[0] # Manipulate string to get column names
        info = [el[i].text_content().replace((name + ' '), '') for el in tr_elements]
        data_dict[name] = info

    df = pd.DataFrame.from_dict(data_dict)
    print(df.head())

    return df


def main():
    scrape_nba_draft_prospects('https://www.nba.com/draft/2020/prospects#/')

if __name__ == "__main__":
    main()
