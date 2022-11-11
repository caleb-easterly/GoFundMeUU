# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os
import requests
import time

# change directory
os.chdir("C:\\Users\\caleb\\OneDrive - University of North Carolina at Chapel Hill\\Documents\\Projects\\Cancer care crowdfunding\\GoFundMeUU")

urls = pd.read_csv('data/urls.txt', sep = '\t', header=None)
urls.rename(columns={0: "URL"})

np.random.seed(17985324)

# first sample to take 
nsamp = 1000

# number of medical campaigns we need
nmed = 100

url_samp = urls.sample(nsamp).reset_index(drop=True)
headers = ["URL", "Category"]
scraped = url_samp.reindex(columns = headers)
scraped["URL"] = url_samp

# keep track of how many we "got"
ngot = 0
for i in range(nsamp):
    if ngot == nmed:
        break
    url = scraped.loc[i, "URL"]
    print("Trying URL #" + str(i))
    # request with max number of attempts
    attempts = 0
    maxattempt = 5
    first_delay = 3
    while attempts < maxattempt:
        try:
            page = requests.get(url)
            # reset attempts
            attempts = 0
            break
        except:
            print("Error with url #" + str(i) + "on attempt #" + str(attempts))
            attempts += 1
            # exponential backoff
            this_delay = first_delay**attempts
            time.sleep(this_delay)
    soup = BeautifulSoup(page.text, 'lxml')
    # campaign type
    try:
        cat = soup.find("a", {"class": "flex-container align-center hrt-link hrt-link--gray-dark"}).text
        scraped.loc[i, "Category"] = cat
    except:
        scraped.loc[i, "Category"] = ""
    if cat == "Medical":
        ngot += 1

output = scraped.query('Category == "Medical"')
output.to_csv("data/qa_100.csv", sep=",")
