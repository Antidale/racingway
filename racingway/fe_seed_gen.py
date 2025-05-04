'''
Code specific to generating Free Enterprise seeds.
'''
import asyncio
import os
import requests

class InvalidFlagString(Exception):
    def __init__(self, message):
        self.message = message

class SeedGenerationError(Exception):
    def __init__(self, message):
        self.message = message 

preset_list = {
    ''
}

class FF4FESeedGen():

    def __init__(self):
        super().__init__("ff4roll")

    async def gen_fe_seed(flags, seed=""):  
        # Send post to generate seed
        # base_url = "http://127.0.0.1:8080"
        # api_key = os.environ['LOCAL_API_KEY']

        base_url = "https://ff4fe.galeswift.com"
        api_key = os.environ['GALESWIFT_API_KEY']

        gen_data = {"flags": flags, "seed": seed}
        post_response = requests.post(f"{base_url}/api/generate?key={api_key}", data=gen_data).json()
        
        # Handle post response
        if post_response["status"] == "error":
            raise InvalidFlagString(post_response["error"])
        if post_response["status"] == "exists":
            seed_id = post_response["seed_id"]
        else:
            assert(post_response["status"] == "ok")
            task_id = post_response["task_id"]
            
            # Wait for seed generation task to complete
            seconds_passed = 0
            while True:
                await asyncio.sleep(2.5)
                seconds_passed += 1
                gen_task = requests.get(f"{base_url}/api/task?key={api_key}&id={task_id}").json()
                if gen_task["status"] in ("pending", "in_progress"):
                    continue
                if gen_task["status"] == "done":
                    seed_id = gen_task["seed_id"]
                    break
                else:
                    assert(gen_task["status"] == "error") 
                    raise SeedGenerationError(gen_task["error"])
            
        # Get the seed info
        seed_info = requests.get(f"{base_url}/api/seed?key={api_key}&id={seed_id}").json()
        if seed_info["status"] == "error":
            raise SeedGenerationError(seed_info["error"])
        return seed_info