"""
Description: Scrape 1000 GoFundMe pages for only title and campaign text.
Results will be used for "ground-truth" verification of classification algorithm. 
Author: Caleb Easterly
"""
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import requests
import re
import os
from is_in_us import is_in_us

# number of medical campaigns we need
nmed_needed = 1000

# change directory
os.chdir("C:\\Users\\caleb\\OneDrive - University of North Carolina at Chapel Hill\\Documents\\Projects\\Cancer care crowdfunding\\GoFundMeUU")

# get urls
urls = pd.read_csv('data/urls.txt', sep = '\t', header=None)
urls.rename(columns={0: "URL"})

# sample lots of urls
np.random.seed(15418942)
nsamp = 50000
url_samp = urls.sample(nsamp).reset_index(drop=True)
headers = ["URL", "Scraped", "Title", "Text"]
scraped = url_samp.reindex(columns = headers)
scraped["URL"] = url_samp

nmed = 0
startsc = time.time()
for i in range(nsamp):
    if nmed == nmed_needed:
        break
    url = scraped.loc[i, "URL"]
    print("Trying URL #" + str(i))
    # try to get HTML. If request fails, sleep and try again
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')
    except:
        time.sleep(0.5)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')
    # campaign type
    try:
        cat = soup.find("a", {"class": "flex-container align-center hrt-link hrt-link--gray-dark"}).text
    except:
        cat = ""
    if cat != "Medical":
        continue
    else:
        scraped.loc[i, "Scraped"] = 1
        # add one to number of med campaigns found on nmed
        nmed = nmed + 1
        # campaign description 
        try:
            container = soup.find("div", {"class": "o-campaign-description"})
            scraped.loc[i, "Text"] = container.text
        except:
            scraped.loc[i, "Text"] = ""
        # campaign title
        try: 
            title_container = soup.find("h1",{"class":"mb0 a-campaign-title"})
            scraped.loc[i, "Title"] = title_container.text
        except:
            scraped.loc[i, "Title"] = ""
        # location
        try:
            location_clean, state, is_us = get_location(soup)
            scraped.loc[i, "Location"] = location_clean
            scraped.loc[i, "State"] = state
            scraped.loc[i, "IsUSA"] = is_us
    time.sleep(np.random.uniform(0.5, 1.5))
stopsc = time.time()
print(stopsc - startsc)
scraped

# only keep scraped/medical
output = scraped.query('Scraped == 1').drop(columns='Scraped')

output.to_excel("scraped_truth.xlsx")
