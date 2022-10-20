from cmath import inf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import requests
from tqdm import  tqdm
import re
from lxml import  etree
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup


def getEmail(homeLink):
    response=requests.get(homeLink)
    text=response.text
    patterns=[
    "[A-Za-z0-9\s]+@[A-Z0-9a-z\s]+.[A-Za-z\s]{2,}",
    "[A-Za-z0-9\s]+\[at\][A-Z0-9a-z\s]+\[dot\][A-Za-z\s]{2,}",
    "[A-Za-z0-9\s]+\(at\)[A-Z0-9a-z\s]+\(dot\)[A-Za-z\s]{2,}",
    "[A-Za-z0-9\s]+at[A-Z0-9a-z\s]+dot[A-Za-z\s]{2,}",]
#     ""
#     "[^><\"\']+@[^><\"\']+\.[^><\"\']+",
#     "[^><\"\']+at[^><\"\']+dot[^><\"\']+",
#     "[^><\"\']+at[^><\"\']+\.[^><\"\']+",
#     "[^><\"\']+@[^><\"\']+dot[^><\"\']+"
    return [re.findall(pattern,text)for pattern in patterns]

def homepage2email(hrefs):
    emails=[]
    for href in tqdm(hrefs):
        try:
            emails.append(getEmail(href))
        except Exception as e:
            print(href+' : '+str(e))
            emails.append([])
    return emails

def crawlPage(userChoices,base_url, to_year, from_year):
    url = base_url+userChoices
    print(url)
    browser= webdriver.Chrome(executable_path="chromedriver")
    browser.get(url)
    
    grbf = Select(browser.find_element(By.ID, "fromyear"))
    grbf.select_by_value(from_year)
    grbf = Select(browser.find_element(By.ID, "toyear"))
    grbf.select_by_value(to_year)

    #you can increase the timeout number(i.e. 120)  if your network is slow
    wait = WebDriverWait(browser, 120)
    waitPath='//*[@id="ranking"]/tbody/tr'
    wait.until(EC.presence_of_all_elements_located((By.XPATH,waitPath)))
    page = etree.HTML(browser.page_source)
    trs = page.xpath(waitPath)
    browser.close()
    return trs

def getUInfo(Utr):
    html_str = etree.tostring(Utr, pretty_print=True, encoding="utf-8")
    parsed_html = BeautifulSoup(html_str)
    info = str(parsed_html.body.text.strip()).split('\n')
    for i in range(len(info)):
        info[i] = info[i].replace(u'\xa0', u'')
    info[1] = info[1][1:]
    return '@'.join(info)



def getUProfsInfos(Uprofs):

    profs=Uprofs.xpath('td/div/div/table/tbody/tr')
    profs=profs[::2] # skip noisy tr
    profsInfos=[prof.xpath('td')for prof in profs] #[professors,infos]  e.g. 30*4
    return [ getProfInfos(profInfos) for profInfos in profsInfos]

def getProfInfos(profInfos):
    personal=profInfos[1]
    pubs=profInfos[2].xpath('small/a/text()')[0]
    adjs=profInfos[3].xpath('small/text()')[0]
    Pname=personal.xpath('small/a[1]/text()')[0]
    homepageLink=personal.xpath('small/a[1]/@href')[0]
    return [Pname,homepageLink,pubs,adjs]