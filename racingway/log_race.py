'''
Code for logging races
'''
import requests
import os

class LogRaceRoom():
    def new_seed_log(room_name, creator_id, description, goal):
        return {
            "UserId": creator_id,
            "RoomName": room_name,
            "RaceType": "FFA",
            "RaceHost": "Racetime.gg",
            "Metadata": {
                "Description": description,
                "Goal": goal
            }
        }
    
class RaceLogger():
    async def log_race_created(room_name, creator, description, goal):
        #default to racingway's discord id
        creator_id = 1375651965371027557
        if creator is not None:
            creator_id = creator.get('full_name')
        payload = LogRaceRoom.new_seed_log(room_name, creator_id, description, goal)
        # url = "https://localhost:5001/api/Races"
        url = "https://free-enterprise-info-api.herokuapp.com/api/Races"
        header = { 'Api-Key': os.environ['FE_Info_Api_Key'] }
        return requests.post(url=url, json=payload, headers=header)