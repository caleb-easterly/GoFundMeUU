
import numpy as np
import pandas as pd
import os

PROJECT_PATH = os.path.realpath("C:/Users/caleb/OneDrive - University of North Carolina at Chapel Hill/Documents/Projects/Cancer care crowdfunding/GoFundMeUU")

discover = pd.read_csv(PROJECT_PATH + "/data/discover_urls.csv", header=None)
sitemap = pd.read_csv(PROJECT_PATH + "/data/urls.txt", header=None, encoding_errors='replace')

discover[0].count()
sitemap[0].count()

merged = pd.merge(sitemap, discover, how='outer', on=0, indicator=True)

merged.groupby(by='_merge').size()



