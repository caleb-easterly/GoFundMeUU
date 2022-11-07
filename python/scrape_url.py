# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import requests
import re
import os
from is_in_us import is_in_us

# change directory
os.chdir("C:\\Users\\caleb\\OneDrive - University of North Carolina at Chapel Hill\\Documents\\Projects\\Cancer care crowdfunding\\GoFundMeUU")

urls = pd.read_csv('data/urls.txt', sep = '\t', header=None)
urls.rename(columns={0: "URL"})

np.random.seed(1247839)
nsamp = 1000000
ngood = 100000
url_samp = urls.sample(nsamp).reset_index(drop=True)

headers = ["URL", "Category", "Full_Scrape", "Position", "Title", "Location", "State", "IsUSA", "Amount_Raised", "Goal", "Number_of_Donators", "Length_of_Fundraising", "FB_Shares", "GFM_hearts", "Text"]
scraped = url_samp.reindex(columns = headers)
scraped["URL"] = url_samp
def get_donation_amounts(soup):
    donation_info_container = soup.find("div",{"class":"o-campaign-sidebar-progress-meter m-progress-meter"})
    amounts = donation_info_container.findChild("h2", {"class": "m-progress-meter-heading"}).text
    extract_amounts = re.match('(\$[\d,]*)\s*raised of ([\$[\d,]*)', amounts)
    raised = re.sub("[$,]", "", extract_amounts.group(1))
    goal = re.sub("[$,]", "", extract_amounts.group(2))
    return raised, goal

# location - test case for later
# test_url = "https://www.gofundme.com/f/k5fdzu-help-chris-breathe"
# page = requests.get(test_url)
# soup = BeautifulSoup(page.text, "lxml")
# organizer = soup.find("div", {"class": "m-campaign-members-main-organizer"})
# person = organizer.find("div", {"class": "m-person-info-content"}).findAll("div", recursive=False)
# # always get last div for location
# location = person[len(person) - 1].text
# # remove comma and get state (or whatever is last word)
# location_clean = re.sub('[\W_]', ' ', location)
# state = location_clean.split().pop()
# # state codes - s/o to https://gist.github.com/JeffPaine/3083347 
# states = { 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
#            'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
#            'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
#            'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
#            'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'}
# is_state_code = state in states

def get_location(soup):
    organizer = soup.find("div", {"class": "m-campaign-members-main-organizer"})
    person = organizer.find("div", {"class": "m-person-info-content"}).findAll("div", recursive=False)

    # always get last div for location
    location = person[len(person) - 1].text

    # remove comma and get state (or whatever is last word)
    location_clean = re.sub('[\W_]', ' ', location)
    state = location_clean.split().pop()
    us = is_in_us(state)
    return location_clean, state, us

startsc = time.time()
ngot = 0
for i in range(nsamp):
    if ngot == ngood:
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
    if cat != "Medical":
        scraped.loc[i, "Full_Scrape"] = False
        continue
    else:
        scraped.loc[i, "Full_Scrape"] = True
        # campaign description 
        try:
            container = soup.find("div", {"class": "o-campaign-description"})
            scraped.loc[i, "Text"] = container.text
        except:
            scraped.loc[i, "Text"] = ""
        # location
        # need organizer first
        try:
            location_clean, state, is_us = get_location(soup)
            scraped.loc[i, "Location"] = location_clean
            scraped.loc[i, "State"] = state
            scraped.loc[i, "IsUSA"] = is_us
        except:
            scraped.loc[i, "Location"] = ""
            scraped.loc[i, "State"] = ""
            scraped.loc[i, "IsUSA"] = False
        # amounts
        try:
            raised, goal = get_donation_amounts(soup)
            scraped.loc[i, "Amount_Raised"] = raised
            scraped.loc[i, "Goal"] = goal
        except:
            scraped.loc[i, "Amount_Raised"] = np.nan
            scraped.loc[i, "Goal"] = np.nan
        # campaign title
        try: 
            title_container = soup.find("h1",{"class":"mb0 a-campaign-title"})
            scraped.loc[i, "Title"] = title_container.text
        except:
            scraped.loc[i, "Title"] = ""
    time.sleep(np.random.uniform(0.2, 1))
    if cat == "Medical" and is_us:
        ngot += 1

stopsc = time.time()
print(stopsc - startsc)
scraped

output = scraped.query('Category == "Medical" & IsUSA').drop(columns='Full_Scrape')
output.to_csv("scraped_082522.csv", sep=",")
