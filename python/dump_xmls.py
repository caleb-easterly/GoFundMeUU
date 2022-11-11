import xml.etree.ElementTree as ET
import glob

# function to take the set of XML files from the GFM sitemap
# and dump associated urls to a text file
def dump_xmls(data_dir, url_fname="urls.txt"):
    # use the namespace
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    ns_url = ns + "url"
    ns_loc = ns + "loc"

    # list of files in the xmls directory
    xmls_path = data_dir + "/xmls/*.xml"
    xml_files = glob.glob(xmls_path)

    # make empty list of URLs to append to
    urls = list()

    # parse the xml tree to get the url
    for f in xml_files:
        xmltree = ET.parse(f)
        xmlroot = xmltree.getroot()
        resources = xmlroot.findall(ns_url)
        urls_tmp = [r.find(ns_loc).text for r in resources]
        urls = urls + urls_tmp

    # write urls to text file
    with open(data_dir + url_fname, 'w') as f:
        for u in urls:
                f.write(f"{u}\n")
