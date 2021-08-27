import requests
from utils import *
from decouple import config

def isUserExists(userName):
    response = __getUser__(userName)

    data = json_extract(response.json(), 'error')

    return len(data) == 0

def getSalesCountForUser(userName):
    response = __getUser__(userName)

    salesCount = json_extract(response.json(), 'sales').pop()

    return int(salesCount)

def __getUser__(userName):
    url = f"https://api.envato.com/v1/market/user:{userName}.json"
    headers = {
        "Authorization": f"Bearer {config('ENVATO_KEY')}"
    }

    response = requests.get(url, headers=headers)

    return response