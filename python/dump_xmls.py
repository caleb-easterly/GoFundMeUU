
import requests
import io
from urllib.request import urlopen
import gzip
import xml.etree.ElementTree as ET
import os
import pandas as pd


# base path for the project
PROJECT_PATH = os.path.realpath("C:/Users/caleb/OneDrive - University of North Carolina at Chapel Hill/Documents/Projects/Cancer care crowdfunding/GoFundMeUU")

# use the namespace
ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
ns_url = ns + "url"
ns_loc = ns + "loc"

urls = list()

for i in range(1, 106):
    xmlname = "sitemap" + str(i) + ".xml"
    xmlpath = os.path.realpath(PROJECT_PATH + "/data/xmls/" + xmlname)
    xmltree = ET.parse(xmlpath)
    xmlroot = xmltree.getroot()
    resources = xmlroot.findall(ns_url)
    urls_tmp = [r.find(ns_loc).text for r in resources]
    urls = urls + urls_tmp

with open(PROJECT_PATH + "/data/" + "urls.txt", 'w') as f:
    for u in urls:
            f.write(f"{u}\n")


# tree1 = 
# root = tree1.getroot()

# # get all second-level nodes
# resources = root.findall(ns_url)
# print(resources)

# # list of xml.gz files, one under each sitemap node 

# print(urls)
