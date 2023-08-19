import os
from requests_ratelimiter import LimiterSession
import requests


ACCESS_TOKEN = os.environ['VK_SERVICE_ACCESS_TOKEN']
API_VERSION = os.environ['VK_API_VERSION']

# session = LimiterSession(per_second=4)


def request_wrapper(command: str, params: dict):
    params['access_token'] = ACCESS_TOKEN
    params['v'] = API_VERSION
    response = requests.get(f'https://api.vk.com/method/{command}', params=params)

    return response.json()
