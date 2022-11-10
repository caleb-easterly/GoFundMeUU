from multiprocessing import Process, Queue, Pool
from campaign import campaign

from campaign import campaign
import pandas as pd
from time import sleep
import os
from random import uniform
import time

# change directory
os.chdir("C:\\Users\\caleb\\OneDrive - University of North Carolina at Chapel Hill\\Documents\\Projects\\Cancer care crowdfunding\\GoFundMeUU")

urls_df = pd.read_csv("data/qa_1000_second_round.csv", sep=",")
urls = urls_df['URL'].tolist()[:100]

# create campaign objects
campaigns = set()

def scrape_campaign(u):
    c = campaign(url=u)
    sleep(uniform(0.2, 0.6))
    return c

if __name__ == '__main__':
    one_start = time.time()
    with Pool(processes=1) as pool:
        campaigns = pool.map(scrape_campaign, urls)
    one_end = time.time()
    t1 = (one_end - one_start)/60

    four_start = time.time()
    with Pool(processes=4) as pool:
        campaigns = pool.map(scrape_campaign, urls)
    four_end = time.time()
    t4 = (four_end - four_start)/60

    print("Time 1 node: " + str(t1))
    print("Time 4 node: " + str(t4))


