
clear

cd "C:\Users\caleb\OneDrive - University of North Carolina at Chapel Hill\Documents\Projects\Cancer care crowdfunding\final_data"
set linesize 120
capture log close
log using make_stata_files.log, text replace

local files filtered_full_samp analytic_file lgbtq_med_campaigns geocodes

foreach f of local files {
	clear
	import delimited "`f'.csv", ///
		encoding("utf-8") bindquote("strict") varnames(1)
	compress
	save `f'.dta, replace
}

log close
