
clear

import delimited qa_100.csv, varnames(1) encoding("utf-8")
save qa_100, replace
clear

import delimited scraped_100qa_111.csv, varnames(1) encoding("utf-8")
rename * *_scraped
rename url_scraped url
merge 1:1 url using qa_100, nogen 

* title
gen title_match = title_scraped == title
tab title_match // all matching except 16, which have simple punctuation mismatches

* amount raised
sum raised_scraped goal_scraped

replace funds_raised = ustrregexra(funds_raised, "[,\\$]", "")
destring funds_raised, replace

replace funding_goal = ustrregexra(funding_goal, "[\\$,NA]", "")
destring funding_goal, replace

gen raised_match = raised_scraped == funds_raised
replace raised_match = . if missing(raised_scrape) | missing(funds_raised)

* how many missing with scrape that shouldn't be missing?
gen badraised = missing(raised_match) & !missing(funding_goal)
tab badraised, missing
browse if badraised

* num donors
replace num_donations = "" if num_donations == "NA"
destring num_donations, replace

gen donor_match = number_of_donors_scraped == num_donations if !missing(num_donations)

* final summar
sum donor_match title_match raised_match






