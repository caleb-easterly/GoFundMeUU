from multiprocessing import Pool
import pandas as pd
from time import sleep
import os
from random import uniform
import time
import argparse
import pickle

# project modules
from campaign import campaign
from get_sitemap import get_sitemap
from dump_xmls import dump_xmls

# change directory
# os.chdir("C:\\Users\\caleb\\OneDrive - University of North Carolina at Chapel Hill\\Documents\\Projects\\Cancer care crowdfunding\\GoFundMeUU")

# urls_df = pd.read_csv("data/qa_1000_second_round.csv", sep=",")
# urls = urls_df['URL'].tolist()[:100]

def scrape_campaign(u):
    c = campaign(url=u)
    sleep(uniform(0.2, 0.6))
    return c

if __name__ == '__main__':
    # command line management
    parser = argparse.ArgumentParser(description='GoFundMe web scraper')
    parser.add_argument('-d', dest='dir', default=".", help="data directory")
    parser.add_argument('-c', dest='ncore', default=1, help='number of cores for multiprocessing')
    parser.add_argument('-t', dest='test', action="store_true", help='testing mode')
    parser.add_argument('-o', dest='outf', default="scraped.px")
    args = parser.parse_args()
    data_dir = os.path.realpath(args.dir)

    # # get xmls from sitemap
    # get_sitemap(data_dir)

    # # read urls from each of the xmls and dump to a single text file
    # dump_xmls(data_dir, url_fname="urls.txt")

    # read urls from the text file
    urlfile = os.path.join(data_dir, "urls.txt")
    urls_df = pd.read_csv(urlfile, sep=",", encoding='latin-1', header=None, names=['URL'])
    urls = urls_df['URL'].tolist()

    if args.test:
        urls = urls[0:100]

    # do the scrape
    ncore = int(args.ncore)
    with Pool(processes=ncore) as pool:
        campaigns = pool.map(scrape_campaign, urls)
    
    # output results
    outf_path = os.path.join(data_dir, args.outf)
    with open(outf_path, "wb") as f:
        pickle.dump(campaigns, f)

    with open(outf_path, "rb") as f:
        a = pickle.load(f)
        print(a)
