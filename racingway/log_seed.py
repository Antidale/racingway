'''
Code for logging generated seeds to feinfo
'''
from .fe_info import FeInfoApi

class LogSeedRequest():
    def new_log_request(seedinfo, race_id, race_name):
        
        return { 
            "userId": 1375651965371027557, 
            "info": { 
                "seed": seedinfo["seed"],
                "version": seedinfo["version"],
                "flags": seedinfo["flags"],
                "verification": seedinfo["verification"],
                "url": seedinfo["url"],
            },
            "raceId": race_id,
            "raceName": race_name
        }

class FeInfoSeedLogger():          
    async def log_rolled_seed(seed_info, race_id, race_name):
        payload = LogSeedRequest.new_log_request(seed_info, race_id, race_name)
        print(payload)
        return await FeInfoApi.log_rolled_seed(payload)
        