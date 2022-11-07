


from campaign import campaign
import pandas as pd

url = "https://www.gofundme.com/f/debre-birhan-covid19-relief-fund"

c = campaign(url)
c.request()
c.scrape_donation_amounts()
c.raised
c.goal


