clear

cd "C:\Users\caleb\OneDrive - University of North Carolina at Chapel Hill\Documents\Projects\Cancer care crowdfunding\final_data"
set linesize 120
capture log close
log using cleanup_analytic_file.log, text replace

use analytic_file
gen origlocation = location
merge m:1 origlocation using geocodes
keep if _merge == 3 // all matched
drop _merge
drop origlocation

tab country
drop if country != "United States"
tab country

* other cleanup
drop fullpagetext
rename v63 c_non_hodgkins_lymphoma_nodash
label variable c_total "total number of cancer words in title or description"
label variable c_any "any cancer words in title or description"
label variable q_total "total number of LGBTQ+ words in title or description"
label variable q_any "any LGBTQ+ words in title or description"
rename c_total csum_total
rename c_any csum_any
rename q_total qsum_total
rename q_any qsum_any

* date
gen date_clean = date(date_created, "MDY")
format date_clean %td
gen month_created = month(date_clean)
gen year_created = year(date_clean)
drop date_created 
rename date_clean date_created

* geocoding
rename error geocoding_error
label variable county "County (geocoded from organizer's location)"
label variable country "Country (geocoded from organizer's location)"
label variable state "State (copied from organizer's location)"
label variable postalcode "Postal/zip code (geocoded from organizer's location)"
label variable geocoding_error "Geocoding failed (reason unknown)"
 
* replace True/False
foreach v of varlist c_* q_* csum_any qsum_any {
	gen `v'_b = 0
	replace `v'_b = 1 if `v' == "True"
	replace `v'_b = . if `v' == ""
	tab `v', summarize(`v'_b)
	drop `v'
	rename `v'_b `v'
}

order url date_created month_created year_created ///
	title status location county state country postalcode geocoding_error raised ///
	goal number_of_donors tag description language1 language2 inenglish isinus

compress
save analytic_file_final_geocoded, replace
export delimited using analytic_file_final_geocoded.csv, delimiter(",") quote replace
log close
