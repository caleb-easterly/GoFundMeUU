
from campaign import campaign
import pandas as pd
from time import sleep

urls = pd.read_csv("data/qa_100.csv", sep=",")

# create campaign objects
campaigns = set()

scraped = urls.copy()
headers = ["URL", "Category", "Title", "Status", "Location", "Raised", "Goal", "Number_of_Donors", "Date_Created", "Tag"]
scraped = scraped.reindex(columns = headers)

i = 0
for u in urls.URL:
    print(u)
    c = campaign(u)
    scraped.loc[i, "Title"] = c.campaign_title
    scraped.loc[i, "Status"] = c.campaign_status
    scraped.loc[i, "Location"] = c.location_string
    scraped.loc[i, "Raised"] = c.raised
    scraped.loc[i, "Goal"] = c.goal
    scraped.loc[i, "Number_of_Donors"] = c.num_donors
    scraped.loc[i, "Date_Created"] = c.date_created
    scraped.loc[i, "Tag"] = c.tag
    scraped.loc[i, "Description"] = c.campaign_desc
    campaigns.add(c)
    i += 1
    sleep(0.2)

scraped.to_csv("data/scraped_100qa_11.7.csv", sep=",")
