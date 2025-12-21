from typing import List
from datetime import datetime, timedelta

from feeder.utility.Logger import Logger

class Commons:

    __logger = Logger.get_logger()
    __apiKey = 'api-key'

    @classmethod
    def build_params(cls, filters: dict = None) -> dict:
        """Method to build common request params required for polygon api"""
        cls.__logger.info('building query parameters for tickers polygon api')
        params = {'apiKey': cls.__apiKey}
        if filters:
            params.update(filters)
        return params

    @classmethod
    def generate_date_range(cls, start_date: str, end_date: str = None) -> List[str]:
        """Method to generate list of dates given a range of format YYYY-MM-DD"""
        date_range = list()
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            end = datetime.today().date() - timedelta(days=1)
        cls.__logger.info(f"building date range starting from: {start_date}, to {end.strftime('%Y-%m-%d')}")
        current = start
        while current <= end:
            date_range.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=1)
        cls.__logger.info(f'date range built. number of dates: {len(date_range)}')
        return date_range