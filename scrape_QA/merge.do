
clear
cd "C:\Users\caleb\OneDrive - University of North Carolina at Chapel Hill\Documents\Projects\Cancer care crowdfunding\GoFundMeUU"

import delimited scrape_QA/qa_100_manual.csv, varnames(1) encoding("utf-8")
save scrape_QA/qa_100_manual, replace
clear

import delimited data/scraped_100qa_11.7.csv, varnames(1) encoding("utf-8")
rename * *_scraped
rename url_scraped url
merge 1:1 url using scrape_QA/qa_100_manual, nogen 

* status
tab status_scraped

* title
gen title_match = title_scraped == title
tab title_match // all matching except 16, which have simple punctuation mismatches

* amount raised
sum raised_scraped goal_scraped

gen raised_match = raised_scraped == funds_raised
tab raised_match

* goal amount
gen goal_match = goal_scraped == funding_goal if status == "active"
tab goal_match

* how many missing with scrape that shouldn't be missing?
gen badraised = missing(raised_match) & status == "active"
tab badraised, missing

* num donors
gen donor_match = number_of_donors_scraped == num_donations if !missing(num_donations)
tab donor_match

* final summar
sum donor_match raised_match goal_match
browse if !raised_match

* 1000
clear
import delimited data/scraped_1000qa2_11.7.csv, varnames(1) encoding("utf-8")