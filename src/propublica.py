import requests
import json

def get_orgs(page=0):
    base_req = 'https://projects.propublica.org/nonprofits/api/v2/search.json?'
    # payload
    payload = {'state[id]': 'PA',
               'c_code[id]': '3', # 501(c)(3)
               'page':page
               }
    # get data
    data = requests.get(base_req, params=payload)
    # return content
    content = json.loads(data.content.decode('utf-8'))
    return content

def extract_org_data(data):
    org_data = data["organizations"]
    org_data = list(map(lambda x: (x['name'], x['sub_name'], x['city'], x['ein']), org_data))
    # filter for Pittsburgh orgs
    # org_data = list(filter(lambda x: x[2] == 'Pittsburgh', org_data))
    return org_data


def list_ein_data(ein):
    """
    $ curl https://projects.propublica.org/nonprofits/api/v2/organizations/142007220.json
    """
    base_req = 'https://projects.propublica.org/nonprofits/api/v2/organizations/{}.json'
    payload = {'output': 'flat',
               }    
    # get data
    data = requests.get(base_req.format(str(ein)))
    # return content
    content = json.loads(data.content.decode('utf-8'))
    return content    

def get_990(ein, year):
    """
    """
    
    return 
