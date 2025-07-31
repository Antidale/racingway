'''
Code for logging races
'''
from .fe_info import FeInfoApi

class LogRaceRoom():
    def new_seed_log(slug, creator_id, description, goal):
        return {
            "UserId": creator_id,
            "RoomName": slug,
            "RaceType": "FFA",
            "RaceHost": "Racetime.gg",
            "Metadata": {
                "Description": description,
                "Goal": goal
            }
        }
    
class RaceLogger():
    async def log_race_created(slug, creator, description, goal):
        #default to racingway's discord id
        creator_id = "1375651965371027557"
        if creator is not None:
            creator_id = creator.get('full_name')
        payload = LogRaceRoom.new_seed_log(slug, creator_id, description, goal)
        return await FeInfoApi.log_race_room(payload)
