# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import time
import requests
import re
import unicodedata
from langdetect import detect
from math import floor
from time import sleep
from random import uniform
import pandas as pd

# main function call - given a url, 
def scrape_campaign(url):
    # create campaign object for given url (does all scraping)
    c = campaign(url=url)
    df = c.dump_campaign_to_df()
    # sleep to attempt to not overload the server
    sleep(uniform(1, 2))
    return df

class campaign:
    """
    Class to scrape and store GoFundMe campaign details.
    Implementation:
        - uses requests library to access page source for a given URL
        - a combination of BeautifulSoup and regex is used to extract specific features
        - data is put into object attributes
        - if extraction fails, attributes are created and filled with missing (empty strings, or '') 
    Features being extracted:
        - campaign title
        - campaign status (accepting new donations vs. not)
        - campaign description
        - donation amounts (raised amount, goal amount)
        - organizer's location
        - campaign description
        - number of donors
        - date created
        - campaign tag (medical vs. emergency, etc.)
    """
    def __init__(self, url):
        print(url)
        self.url = url
        self.request()
        self.scrape_tag()
        self.scrape_campaign_title()
        self.scrape_campaign_status()
        self.scrape_campaign_desc()
        self.scrape_campaign_desc_lang()
        self.scrape_donation_amounts()
        self.scrape_date_created()
        self.scrape_location()
        self.scrape_num_donors()
        self.soup = ""
    def request(self, maxattempt=5, firstdelay=3):
        attempts = 0
        success = 0
        while attempts < maxattempt:
            try:
                r = requests.get(self.url)
                if r.ok == True:
                    success = 1
                else:
                    raise("bad request. code: " + r.status_code)
                break
            except:
                print("Error with url " + str(self.url) + "on attempt #" + str(attempts))
                attempts += 1
                # exponential backoff
                this_delay = firstdelay**attempts
                time.sleep(this_delay)
        if success == 1:
            # see https://stackoverflow.com/questions/36833357/python-correct-encoding-of-website-beautiful-soup
            encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
            self.soup = BeautifulSoup(r.content, "html.parser", from_encoding=encoding)
            self.pagetext_raw = r.text
            # store full pagetext in case it's needed later
            pagetext = self.soup.get_text()
            # remove newlines and tab characters
            self.pagetext = re.sub('[\\t\\n]', '', pagetext)
        else:
            self.pagetext = ""
            self.soup = ""
    # methods for scraping data
    def scrape_campaign_status(self):
        str_no_new_donations = '.*The organizer has currently disabled new donations.*'
        str_not_accepting = '.*This fundraiser is no longer accepting donations.*'
        if re.match(str_no_new_donations, self.pagetext):
            self.campaign_status = "no new donations"
        elif re.match(str_not_accepting, self.pagetext):
            self.campaign_status = "not accepting"
        else:
            self.campaign_status = "active"
    def scrape_donation_amounts(self):
        try:
            # old stuff
            # self.goal = re.search(r'\\"goal_amount\\":(\d*)', self.pagetext).group(1)
            # self.raised = re.search(r'\\"goal_amount\\":(\d*)', self.pagetext).group(1)
            # amounts = donation_info_container.findChild("p", {"class": "m-progress-meter-heading"}).text
            # raised = re.sub("[$,]", "", extract_amounts.group(1))
            # goal = re.sub("[$,]", "", extract_amounts.group(2))

            # use soup to find the heading to the progress meter,
            # which contains the raised and goal amounts
            amounts = self.soup.find("p",{"class":"m-progress-meter-heading"})
            # normalize to unicode - removes the non-breaking space
            amount_text = unicodedata.normalize('NFKD', amounts.text)

            # remove money characters and the dot thing
            amount_text = re.sub("[$£€,•\.]", "", amount_text)

            # remove multiple spaces
            amount_text = ' '.join(amount_text.split())
            
            # try to match raised and goal separately
            # (because sometimes there is only a raised amount)
            raised = re.match('(\d*).* raised', amount_text)
            goal = re.match('^.*raised of (\d*) goal.*$', amount_text)
            if raised != None:
                self.raised = raised.group(1)
            else:
                self.raised = ""
            if goal != None:
                self.goal = goal.group(1)
            else:
                self.goal = ""
        # catch any unexpected exceptions
        except:
            self.raised = ""
            self.goal = ""
    def scrape_location(self):
        try:
            organizer = self.soup.find("div", {"class": "m-campaign-members-main-organizer"})
            person = organizer.find("div", {"class": "m-person-info-content"}).findAll("div", recursive=False)
            # always get last div for location
            self.location_string = person[len(person) - 1].text
            # remove comma and get state (or whatever is last word)
            location_clean = re.sub(',', '', self.location_string)
            self.state = location_clean.split().pop()
            # state codes - s/o to https://gist.github.com/JeffPaine/3083347 
            # move to utils at some point 
            states = { 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
                    'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
                    'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
                    'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                    'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'}
            self.is_us_state_code = self.state in states
        except:
            self.location_string = ""
            self.state = ""
            self.is_us_state_code = ""
    # campaign description 
    def scrape_campaign_desc(self):
        try:
            campaign_desc = self.soup.find("div", {"class": "o-campaign-description"}).text
            # remove the always-present "read more" at the end of the description
            # (always there even though there's no more to read)
            campaign_desc = re.sub('Read more', '', campaign_desc)
            # remove newlines and tab characters
            self.campaign_desc = re.sub('[\\t\\n]', '', campaign_desc)
        except:
            self.campaign_desc = ""
    # campaign language
    def scrape_campaign_desc_lang(self):
        if self.campaign_desc != "":
            try:
                # previously used detect_langs and assessed prob of english
                # but didn't work that well for campaigns that had both english and non-english words
                # new solution is to split in half, since this is a common pattern
                length_half_desc = floor(len(self.campaign_desc)/2)
                first_half = self.campaign_desc[0:length_half_desc]
                second_half = self.campaign_desc[length_half_desc:]
                first_lang = detect(first_half)
                second_lang = detect(second_half)
                self.lang1 = first_lang
                self.lang2 = second_lang
                self.in_english = first_lang == "en" or second_lang == "en"
            except:
                self.lang1 = ""
                self.lang2 = ""
                self.in_english = ""
        else:
            self.lang1 = ""
            self.lang2 = ""
            self.in_english = ""
    # campaign title
    def scrape_campaign_title(self):
        try: 
            self.campaign_title = self.soup.find("header",{"class":"p-campaign-header"}).text
        except:
            self.campaign_title = ""
    # number of donations
    def scrape_num_donors(self):
        # doesn't seem to work with soup since the number of donors is loaded dynamically
        # use simple re - found pattern by searching test page
        try:
            self.num_donors = re.search(r'\\"donation_count\\":(\d*)', self.pagetext_raw).group(1)
        except:
            self.num_donors = ""
    def scrape_date_created(self):
        try:
            date_raw = self.soup.find("span", {"class": "m-campaign-byline-created a-created-date show-for-large"}).text
            self.date_created = str.strip(date_raw, "Created ")
        except:
            self.date_created = ""
    def scrape_tag(self):
        try:
            tag_raw = self.soup.find("a", {"class": "flex-container align-center hrt-link hrt-link--gray-dark"}).text
            self.tag = str.strip(tag_raw)
        except:
            self.tag = ""
    def dump_campaign_to_df(self):
        headers = ["URL", "Title", "Status", "Location", "Raised", "Goal", 
            "Number_of_Donors", "Date_Created", "Tag", "Description", "FullPageText", "Language1", "Language2", "InEnglish"]
        camp_df = pd.DataFrame(columns=headers)
        camp_df.loc[0, "URL"] = self.url
        camp_df.loc[0, "Title"] = self.campaign_title
        camp_df.loc[0, "Status"] = self.campaign_status
        camp_df.loc[0, "Location"] = self.location_string
        camp_df.loc[0, "State"] = self.state
        camp_df.loc[0, "IsInUS"] = self.is_us_state_code
        camp_df.loc[0, "Raised"] = self.raised
        camp_df.loc[0, "Goal"] = self.goal
        camp_df.loc[0, "Number_of_Donors"] = self.num_donors
        camp_df.loc[0, "Date_Created"] = self.date_created
        camp_df.loc[0, "Tag"] = self.tag
        camp_df.loc[0, "Description"] = self.campaign_desc
        camp_df.loc[0, "FullPageText"] = self.pagetext
        camp_df.loc[0, "Language1"] = self.lang1
        camp_df.loc[0, "Language2"] = self.lang2
        camp_df.loc[0, "InEnglish"] = self.in_english
        return camp_df
