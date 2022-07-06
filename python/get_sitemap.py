
import requests
import io
from urllib.request import urlopen
import gzip
import xml.etree.ElementTree as ET
import os

# base path for the project
PROJECT_PATH = os.path.realpath("C:/Users/caleb/OneDrive - University of North Carolina at Chapel Hill/Documents/Projects/Cancer care crowdfunding/GoFundMeUU")

# get the sitemap
url = urlopen("https://www.gofundme.com/sitemap.xml")
tree = ET.parse(url)
root = tree.getroot()

# use the namespace
ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
ns_stmap = ns + "sitemap"
ns_loc = ns + "loc"

# get all second-level nodes
resources = root.findall(ns_stmap)

# list of xml.gz files, one under each sitemap node 
zipped = [r.find(ns_loc).text for r in resources]

# drop marketing
marketing_bad = 'https://www.gofundme.com/sitemaps/www/sitemap_marketing.xml.gz'
clean_url_zipped = list(filter(marketing_bad.__ne__, zipped))

# write each XML to a new file
for cuz in clean_url_zipped:
    # request 
    r = requests.get(cuz)

    # check request - shouldn't have any bads
    if r.ok == False:
        raise("bad request. code: " + r.status_code)
    r_io = io.BytesIO(r.content)

    # read and write - TODO will operate in the same loop
    with gzip.open(r_io, "r") as f:
        content = f.read()
        newfile = os.path.realpath(PROJECT_PATH + "/data/xmls/" + str.removeprefix(str.removesuffix(cuz, ".gz"), "https://www.gofundme.com/sitemaps/www/"))
        with open(newfile, "wb") as f:
            f.write(content)
