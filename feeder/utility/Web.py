import ssl
from typing import Optional

import json

import aiohttp
import certifi
import requests

from feeder.utility.Logger import Logger

class Web:

    __logger = Logger.get_logger()
    __ssl_context = ssl.create_default_context(cafile=certifi.where())

    @classmethod
    def request(cls, method: str, url: str, headers: Optional[dict], params:dict, body: Optional[dict]) -> dict:
        """ Method to make an  HTTP request """
        response_data = dict()
        try:
            response = requests.request(method=method, url=url, headers=headers, params=params, data=body)
            response_data =  json.loads(response.text)
        except Exception as exception:
            cls.__logger.exception(exception)
        return response_data

    @classmethod
    async def request_asynchronous(cls, method: str, url: str, headers: Optional[dict], params:dict, body: Optional[dict]):
        """Method to make asynchronous HTTP request"""
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=cls.__ssl_context)) as session:
            async with session.request(method=method, url=url, headers=headers, data=body, params=params) as response:
                return await response.text()

