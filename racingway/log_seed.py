'''
Code for logging generated seeds to feinfo
'''
import requests
import os

class LogSeedRequest():
    def new_log_request(seedinfo):
        
        return { 
            "userId": 1375651965371027557, 
            "info": { 
                "seed": seedinfo["seed"],
                "version": seedinfo["version"],
                "flags": seedinfo["flags"],
                "verification": seedinfo["verification"],
                "url": seedinfo["url"],
            }
        }

class FeInfoSeedLogger():          
    async def log_rolled_seed(seed_info):
        payload = LogSeedRequest.new_log_request(seed_info)
        # url = "https://localhost:5001/api/Seed"
        url = "https://free-enterprise-info-api.herokuapp.com/api/Seed"
        header = { 'Api-Key': os.environ['FE_Info_Api_Key'] }
        return requests.post(url=url, json=payload, headers=header)
        