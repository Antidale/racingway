'''
Code specific to generating Free Enterprise seeds.
'''
import asyncio
import requests
from . import fe_hosts

class InvalidFlagString(Exception):
    def __init__(self, message):
        self.message = message

class SeedGenerationError(Exception):
    def __init__(self, message):
        self.message = message 

class FF4FESeedGen():
    async def gen_fe_seed(flags, host, seed=""):  
        api_info = fe_hosts.get_api_info(host)

        gen_data = {"flags": flags, "seed": seed}
        post_response = requests.post(f"{api_info.base_url}/api/generate?key={api_info.api_key}", data=gen_data).json()
        
        # Handle post response
        if post_response["status"] == "error":
            raise InvalidFlagString(post_response["error"])
        if post_response["status"] == "exists":
            seed_id = post_response["seed_id"]
        else:
            assert(post_response["status"] == "ok")
            task_id = post_response["task_id"]
            
            # Wait for seed generation task to complete
            iterations = 0
            while True:
                if iterations > 100:
                    raise TimeoutError("seed is failing to generate, aborting")
                
                await asyncio.sleep(2.5)
                iterations += 1
                
                gen_task = requests.get(f"{api_info.base_url}/api/task?key={api_info.api_key}&id={task_id}").json()
                
                match gen_task["status"]:
                    case "error":
                        raise SeedGenerationError(gen_task["error"])
                    case "done":
                        seed_id = gen_task["seed_id"]
                        break
                    case _:
                        continue                  
            
        # Get the seed info
        seed_info = requests.get(f"{api_info.base_url}/api/seed?key={api_info.api_key}&id={seed_id}").json()
        if seed_info["status"] == "error":
            raise SeedGenerationError(seed_info["error"])
        return seed_info