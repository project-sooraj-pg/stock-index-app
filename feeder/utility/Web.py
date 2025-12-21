from typing import Optional

import json
import requests

from feeder.utility.Logger import Logger

class Web:

    __logger = Logger.get_logger()

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
