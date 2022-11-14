# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import re
import os
from campaign import campaign
import pickle
from multiprocessing import Pool

# change directory
os.chdir("C:\\Users\\caleb\\OneDrive - University of North Carolina at Chapel Hill\\Documents\\Projects\\Cancer care crowdfunding\\GoFundMeUU")

headers = ["URL", "Title", "Status", "Location", "Raised", "Goal", 
    "Number_of_Donors", "Date_Created", "Tag", "Description", "Language1", "Language2", "InEnglish"]
scraped = pd.DataFrame(columns = headers)

def extract_to_series(c):
    crow = pd.DataFrame(columns=headers)
    crow.loc[0, "URL"] = c.url
    crow.loc[0, "Title"] = c.campaign_title
    crow.loc[0, "Status"] = c.campaign_status
    crow.loc[0, "Location"] = c.location_string
    crow.loc[0, "State"] = c.state
    crow.loc[0, "IsInUS"] = c.is_us_state_code
    crow.loc[0, "Raised"] = c.raised
    crow.loc[0, "Goal"] = c.goal
    crow.loc[0, "Number_of_Donors"] = c.num_donors
    crow.loc[0, "Date_Created"] = c.date_created
    crow.loc[0, "Tag"] = c.tag
    crow.loc[0, "Description"] = c.campaign_desc
    crow.loc[0, "Language1"] = c.lang1
    crow.loc[0, "Language2"] = c.lang2
    crow.loc[0, "InEnglish"] = c.in_english
    return crow

fpath = "C:\\Users\\caleb\\OneDrive - University of North Carolina at Chapel Hill\\Documents\\Projects\\Cancer care crowdfunding\\results_11.12.22\\t2\\c3lgbt-data\\scraped.px"
with open(fpath, "rb") as f:
    campaigns = pickle.load(f)
    campaigns = campaigns[:10000]
    # with Pool(processes=4) as pool:
    rows = [extract_to_series(c) for c in campaigns]
    df = pd.concat(rows, ignore_index=True)

with open("data/full_pull.csv", "w", encoding="utf-8") as fp:
    df.to_csv(fp, index=False, line_terminator="\n", encoding="utf-8")

# scraped = pd.read_csv("scraped_081822.csv", index_col=0, usecols=["URL", 'Text', 'Goal', 'Amount_Raised'])
# assign most likely language
# def assign_lang(text):
#     return detect(str(text))
# scraped["Lang"] = [assign_lang(str(v)) for k, v in scraped.Text.items()] 

# scraped["TextLower"] = scraped.Text.str.lower().apply(str)
# scraped["LGBTQ_core"] = scraped["TextLower"].str.contains(r"\bgay\b|\blesbian\b|\bbisexual\b|\bqueer\b|\btransgender\b|\bnonbinary\b|\btrans\b|\bLGBT.*\b")
# scraped["LGBTQ_addnl"] = scraped["TextLower"].str.contains(r"\bhis husband\b|\bher wife\b|\bhis boyfriend\b|\bher girlfriend\b")
# scraped["LGBTQ_total"] = scraped.LGBTQ_core | scraped.LGBTQ_addnl
# scraped["cancer"] = scraped["TextLower"].str.contains("cancer")

# # crosstab
# narrow = scraped.query('Lang == "en" & Text != ""')
# pd.crosstab(narrow.LGBTQ_total, narrow.cancer, margins=True)

# # crosstab normalized
# pd.crosstab(narrow.LGBTQ_total, narrow.cancer, margins=True, normalize="all")

# hits = scraped.query("LGBTQ_total & cancer")
# hits.to_csv("lgbtq_cancer.csv")

# ## full table
# scraped.drop(columns="TextLower").to_excel("full_5k_scraped.xlsx")
