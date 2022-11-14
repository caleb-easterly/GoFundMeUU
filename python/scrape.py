from multiprocessing import Pool
import pandas as pd
import os
import argparse
import pickle
from langdetect import DetectorFactory

# project modules
from campaign import scrape_campaign
from get_sitemap import get_sitemap
from dump_xmls import dump_xmls

if __name__ == '__main__':
    # command line management
    parser = argparse.ArgumentParser(description='GoFundMe web scraper')
    parser.add_argument('-d', dest='dir', default=".", help="data directory")
    parser.add_argument('-c', dest='ncore', default=1, help='number of cores for multiprocessing')
    parser.add_argument('-t', dest='test', action="store_true", help='testing mode')
    parser.add_argument('-o', dest='outf', default="scraped", help="outfile name")
    parser.add_argument('-x', dest="getxml", action="store_true", help="download the xmls and update the url file")
    args = parser.parse_args()
    data_dir = os.path.realpath(args.dir)

    if args.getxml:
        # get xmls from sitemap
        get_sitemap(data_dir)

        # read urls from each of the xmls and dump to a single text file
        dump_xmls(data_dir, url_fname="urls.txt")

    # read urls from the text file
    urlfile = os.path.join(data_dir, "urls.txt")
    urls_df = pd.read_csv(urlfile, sep=",", encoding='latin-1', header=None, names=['URL'])
    urls = urls_df['URL'].tolist()

    # take a small part of the urls for testing purposes
    if args.test:
        urls = urls[0:100]

    # set seed for language detection for reproducibility
    DetectorFactory.seed = 10432987

    # do the scrape
    ncore = int(args.ncore)
    with Pool(processes=ncore) as pool:
        campaigns = pool.map(scrape_campaign, urls)

    # combine results into big dataframe
    df = pd.concat(campaigns, ignore_index=True)

    # output results both as csv and pickle
    outf_pickle = os.path.join(data_dir, args.outf) + ".pkl"
    with open(outf_pickle, "wb") as fp:
        pickle.dump(df, fp)

    outf_csv = os.path.join(data_dir, args.outf) + ".csv"
    with open(outf_csv, "w", encoding="utf-8") as fc:
        df.to_csv(fc, index=False, line_terminator='\n', encoding='utf-8')
