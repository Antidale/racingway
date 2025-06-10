'''
Code for logging generated seeds to feinfo
'''
from .fe_info import FeInfoApi

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
        return await FeInfoApi.log_rolled_seed(payload)
        