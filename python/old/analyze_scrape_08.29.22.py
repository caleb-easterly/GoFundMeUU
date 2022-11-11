# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import re
import os
from langdetect import detect, detect_langs, DetectorFactory
from is_in_us import is_in_us

# language
DetectorFactory.seed = 0

# change directory
os.chdir("C:\\Users\\caleb\\OneDrive - University of North Carolina at Chapel Hill\\Documents\\Projects\\Cancer care crowdfunding\\GoFundMeUU")

scraped = pd.read_csv("scraped_082522.csv", index_col=0, usecols=["URL", 'Text', 'Goal', 'Amount_Raised'])

# assign most likely language
def assign_lang(text):
    try:
        lang = detect(str(text))
    except:
        lang = "" 
    return lang

scraped["Lang"] = [assign_lang(str(v)) for k, v in scraped.Text.items()] 

scraped["TextLower"] = scraped.Text.str.lower().apply(str)
scraped["LGBTQ_core"] = scraped["TextLower"].str.contains(r"\bgay\b|\blesbian\b|\bbisexual\b|\bqueer\b|\btransgender\b|\bnonbinary\b|\btrans\b|\bLGBT.*\b")
scraped["LGBTQ_addnl"] = scraped["TextLower"].str.contains(r"\bhis husband\b|\bher wife\b|\bhis boyfriend\b|\bher girlfriend\b")
scraped["LGBTQ_total"] = scraped.LGBTQ_core | scraped.LGBTQ_addnl
# identify campaigns based on mentioning cancer(s) or tumor(s)
scraped["cancer"] = scraped["TextLower"].str.contains("cancer")

# crosstab
narrow = scraped.query('Lang == "en" & Text != ""')
pd.crosstab(narrow.LGBTQ_total, narrow.cancer, margins=True)

# crosstab normalized
pd.crosstab(narrow.LGBTQ_total, narrow.cancer, margins=True, normalize="all")

hits = scraped.query("LGBTQ_total & cancer")
hits.to_excel("lgbtq_cancer_100k.xlsx")

## full table
scraped.drop(columns="TextLower").to_excel("full_100k_scraped.xlsx")
