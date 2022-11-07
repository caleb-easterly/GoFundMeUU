# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os

# change directory
os.chdir("C:\\Users\\caleb\\OneDrive - University of North Carolina at Chapel Hill\\Documents\\Projects\\Cancer care crowdfunding\\GoFundMeUU")

urls = pd.read_csv('data/urls.txt', sep = '\t', header=None)
urls.rename(columns={0: "URL"})

np.random.seed(17985324)
nsamp = 150
url_samp = urls.sample(nsamp).reset_index(drop=True)
url_samp.to_csv('data/urls150.txt', sep='\t')

