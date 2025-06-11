'''
Centralized code for calling endpoints for the fe info api
'''
import requests
import os

base_url = "https://free-enterprise-info-api.herokuapp.com/api/"
header = { 'Api-Key': os.environ['FE_Info_Api_Key'] }

is_debug = False
try:
    is_debug = os.environ['racingway_debug']
except Exception:
    is_debug = False

if (is_debug):
    base_url = "https://localhost:5001/api/"
    header = { 'Api-Key': os.environ['FE_Info_Local_Key'] }
    

class FeInfoApi():
    async def log_rolled_seed(payload):
        url = base_url + "Seed"
        return requests.post(url=url, json=payload, headers=header)
    
    async def log_race_room(payload):
        url = base_url + "Races"

        if(is_debug):
            return requests.post(url=url, json=payload, headers=header, verify=False)
        else:
            return requests.post(url=url, json=payload, headers=header)