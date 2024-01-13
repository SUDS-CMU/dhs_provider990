import pandas as pd
import json
import nltk
import string
import csv
from fuzzywuzzy import fuzz

from src.propublica import get_orgs, extract_org_data, list_ein_data

def read_csv_as_tuples(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data.append(tuple(row))
    return data


if __name__ == "__main__":

    # ----------------------------
    # return data from first page of pro publica API request data
    QUERY_API = False
    if QUERY_API:
        data = get_orgs(page=0)
        # number of returned pages
            # NOTE: read about API pagination here:
            # https://nordicapis.com/everything-you-need-to-know-about-api-pagination/
        total_pages = data['num_pages']
        # collect (name, ein) for each organization list from each page
        org_id_list = extract_org_data(data)
        for page in range(1,total_pages):
            data = get_orgs(page=page)
            org_id_list += extract_org_data(data)
        # write to txt file
        with open("data/all_providers.csv", 'w') as f:
            for org in org_id_list:
                f.write('{},{},{},{}\n'.format(org[0], org[1], org[2], org[3]))
    
    # ----------------------------
    # read organizations of interest
    BUILD_ORG_MAP = False
    if BUILD_ORG_MAP:

        # for each org of interest, check if name matches names listed from Propublica
        with open("data/MPERContractedProviderList.txt") as f:
            dhs_orgs = f.read().split("\n")
        dhs_orgs = list(map(lambda x: (x.split(",")[0], ",".join(x.split(",")[1:])), dhs_orgs))
        
        # read orgs tracked by propublica
        propublica_orgs = read_csv_as_tuples("data/all_providers.csv")

        # for each dhs org, check if exists in propublica orgs
        with open("data/MPERContractedProvider_Updated.csv", 'w') as f:
            f.write('MPER Provider ID,DHS Provider Name,Potential Match Org Name,City,EIN,Name Match Score\n')
            for org in dhs_orgs:
                lev_d = []
                for i, org1 in enumerate(propublica_orgs):
                    similarity_score = fuzz.ratio(org[1].lower().replace(',','').replace('.',''), 
                                                org1[0].lower().replace(',','').replace('.',''))
                    lev_d.append((i, similarity_score))
                # return top 10 closest matches
                lev_d = sorted(lev_d, key=lambda x: x[1], reverse=True)[0:5]
                # only return those with similarity score greater than 50%
                lev_d = list(filter(lambda x: x[1] > 85, lev_d))
                # if empty, write "None"
                if len(lev_d) > 0:
                    for val in lev_d:
                        # write dhs_org, matching org name, matching org sub name, city, ein, match score
                        f.write('{},{},{},{},{},{}\n'.format(org[0],
                                                        string.capwords(org[1]).replace(',',''),
                                                        propublica_orgs[val[0]][0].replace(',',''), 
                                                        propublica_orgs[val[0]][2].replace(',',''),
                                                        propublica_orgs[val[0]][3].replace(',',''),
                                                        val[1]))
                else:
                    # no matches
                    f.write('{},{},No Matches,,,\n'.format(org[0], 
                                                        string.capwords(org[1]).replace(',','')))
                # break

    # --------------------------------------------------------
    # for each DHS org with manually confirmed matched org, establish mapping
    data = pd.read_csv("data/MPERContractedProvider_ManualConfirmation.csv")
    org_mapping = {}
    for org in data["DHS Provider Name"].drop_duplicates():
        org_data = data[data["DHS Provider Name"] == org]
        # filter for exact manual confirmed matches 
        org_data = org_data[org_data["Confirmation"] == 1]
        # check that exactly one record remains
        if len(org_data) != 1:
            # print("---- Org missing exact match: {} -----".format(org))
            continue
        # append match to org_mapping
        org_mapping[org] = int(org_data["EIN"].values[0])
        # break

    # Writing to sample.json
    with open("data/organizationEIN_map.json", "w") as outfile:
        outfile.write(json.dumps(org_mapping, indent=2))

    # --------------------------------------------------------
    # for each DHS org with matched org, retrieve 990 data

    fields = {
        # General 
        "Tax Year": "tax_prd_yr",
        # Revenue
        "Contributions and Grants":"totcntrbgfts",
        "Program service revenue":"totprgmrevnue",
        "Investment Income":"invstmntinc",
        "Total Revenue":"totrevenue",
        # Expenses
        "Compensation of current officers, directors, etc":"compnsatncurrofcr",
        "Payroll Tax":"payrolltx",
        "Professional fundraising fees":"profndraising",
        "Total Functional Expenses":"totfuncexpns",
        # Balance Sheet
        "Total Assets":"totassetsend",
        "Total Liabilities":"totliabend"
    }
    # extract data for each organization
    org_990 = []
    for org, ein in org_mapping.items():
        data = list_ein_data(ein=ein)
        data = list(filter(lambda x: x["tax_prd_yr"] in [2019, 2020, 2021], data["filings_with_data"]))
        # extract data for each available filing
        for f in data:
            id_fields = {"Organization":org, "EIN":ein}
            temp = {k:f.get(v) for k,v in fields.items()}
            temp = {**id_fields, **temp}
            org_990.append(temp)
        # break
    # write 990 data as dataframe
    data_990 = pd.DataFrame(org_990)
    data_990.to_csv("data/Organization990.csv")
