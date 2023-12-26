
import pandas as pd
import json

from src.propublica import get_orgs, extract_org_data

if __name__ == "__main__":

    # return data from first page of pro publica API request data
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
    with open("data/all_providers.txt", 'w') as f:
        for org in org_id_list:
            f.write('{}, {}\n'.format(org[0], org[1]))
    # read organizations of interest
    with open("data/MPERContractedProvider.txt") as f:
        dhs_orgs = f.read().split("\n")
    # remove indices
    dhs_orgs = list(map(lambda x: " ".join(x.split(",")[1:]), dhs_orgs))
    


