
from campaign import campaign
import pandas as pd
from time import sleep
import os

# change directory
os.chdir("C:\\Users\\caleb\\OneDrive - University of North Carolina at Chapel Hill\\Documents\\Projects\\Cancer care crowdfunding\\GoFundMeUU")

urls = pd.read_csv("data/qa_1000_second_round.csv", sep=",")

# create campaign objects
campaigns = set()

scraped = urls.copy()
headers = ["URL", "Title", "Status", "Location", "Raised", "Goal", 
    "Number_of_Donors", "Date_Created", "Tag", "Description", "Language1", "Language2", "InEnglish"]
scraped = scraped.reindex(columns = headers)

i = 0
for u in urls.URL:
    print(u)
    c = campaign(u)
    scraped.loc[i, "Title"] = c.campaign_title
    scraped.loc[i, "Status"] = c.campaign_status
    scraped.loc[i, "Location"] = c.location_string
    scraped.loc[i, "State"] = c.state
    scraped.loc[i, "IsInUS"] = c.is_us_state_code
    scraped.loc[i, "Raised"] = c.raised
    scraped.loc[i, "Goal"] = c.goal
    scraped.loc[i, "Number_of_Donors"] = c.num_donors
    scraped.loc[i, "Date_Created"] = c.date_created
    scraped.loc[i, "Tag"] = c.tag
    scraped.loc[i, "Description"] = c.campaign_desc
    scraped.loc[i, "Language1"] = c.lang1
    scraped.loc[i, "Language2"] = c.lang2
    scraped.loc[i, "InEnglish"] = c.in_english
    campaigns.add(c)
    i += 1
    sleep(0.2)

scraped.to_csv("data/scraped_1000qa2_11.7.csv", sep=",")