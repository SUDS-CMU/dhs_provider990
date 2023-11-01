### DHS Provider 990 Data Pipeline

This project will depend on functionality provided by [Propublica](https://projects.propublica.org/nonprofits/api) NonProfit Explorer API to retrieve 990 form data for set of providers


**Overview**
Given a list of Provider names:
- read list of provider names from source file
- collect IRS 990 data from last three available years
- extract following fields:
    - ...
- standardize data
- specify summary statistics 
- write data to ...?


**Assets**
- source file: ./data/providers.csv
- output: ./data/summary.csv


**Propublica API: Mapping IRS 990 fields to codes**
- [ ] Use [IRS 990 Code Mapping](https://www.irs.gov/pub/irs-soi/12eofinextractdoc.xls) to retrieve codes we are interested in seeing for DHS providers
    - write as `\n` delimited .txt file under `./data/assets/`

**Code Structure**
- [ ] `./src/propublica.py`: methods utilizing [Propublica](https://projects.propublica.org/nonprofits/api) NonProfit Explorer API
    - [ ] `retrieve_providerein()`: retrieve IRS EIN for all providers, given name.
        - see documentation related to "Search Method"
	- example: 'curl https://projects.propublica.org/nonprofits/api/v2/search.json?c_code%5Bid%5D=3&state%5Bid%5D=PA&city%5Bid%5D=PITTSBURGH'
    - [ ] `verify_provider990()`: given EIN, verify that ProPublica has 990 filings for provider for last 3 years
        - see documentation related to "Organization Method"
    - [ ] `retrieve_990fieldset()`: given EIN, tax year, and set of field names, retrieve data
	- see documentation related to "Filing Object"
    - [ ] method to collect 990 and provider identifier data in standardized format





