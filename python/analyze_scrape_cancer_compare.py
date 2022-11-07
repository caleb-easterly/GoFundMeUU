# -*- coding: utf-8 -*-

import pandas as pd
import os

# change directory
os.chdir("C:\\Users\\caleb\\OneDrive - University of North Carolina at Chapel Hill\\Documents\\Projects\\Cancer care crowdfunding\\GoFundMeUU")

scraped = pd.read_csv("scraped_082522.csv", index_col=0, usecols=["URL", 'Text', 'Goal', 'Amount_Raised'])

scraped["TextLower"] = scraped.Text.str.lower().apply(str)
# identify campaigns based on mentioning cancer(s) or tumor(s)
# build string of cancer terms
with open("python\\cancer_terms_silver.csv") as f:
    terms = [elem.strip() for elem in f.readlines()]
    middle = r'.*\b|\b'.join(terms)
    # form string - also allow for cancer within words (for links, hashtags, etc.)
    cancer_detect = r'cancer|' + r'\b' + middle + r'.*\b'

scraped["cancer_only"] = scraped["TextLower"].str.contains("cancer")
scraped["cancer_all"] = scraped["TextLower"].str.contains(cancer_detect)

# crosstab
pd.crosstab(scraped.cancer_only, scraped.cancer_all, margins=True)

# matched 
scraped.query("cancer_only == 0 & cancer_all == 1")
scraped.cancer_only.mean()
scraped.cancer_all.mean()

## full table
scraped.drop(columns="TextLower").to_excel("cancer_matching.xlsx")
