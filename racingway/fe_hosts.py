# add methods for getting information
import os

class ApiHost:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

def get_api_info(hostType):
    hostType = hostType.upper()
    if hostType not in ["MAIN", "GALESWIFT", "LOCAL"]:
        raise NotImplementedError(f'{hostType} is not implemented yet')
    
    url = ''
    if hostType == "MAIN":
        url = 'http://ff4fe.com'
    elif hostType == "GALESWIFT":
        url = 'https://ff4fe.galeswift.com'
    else:
        url = 'http://127.0.0.1:8080'
    
    return ApiHost(url, os.environ[f'{hostType}_API_KEY'])
