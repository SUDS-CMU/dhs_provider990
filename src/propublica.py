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
    org_data = list(map(lambda x: (x['name'], x['ein']), org_data))
    return org_data

def get_990(ein, year):
    """
    """
    
    return 
