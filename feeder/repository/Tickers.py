import time
from datetime import  date
from typing import List, Optional

from feeder.utility.Web import Web
from feeder.utility.Logger import Logger
from feeder.utility.Commons import Commons
from feeder.utility.Configuration import Configuration

class Tickers:

    __tickers = list()
    __logger = Logger.get_logger()
    __configuration = Configuration.load_from_file()
    __tickers_init_url = __configuration['gather']['data-source']['tickers']['url']
    __tickers_overview_init_url = __configuration['gather']['data-source']['ticker-overview']['url']

    @classmethod
    def get_tickers(cls) -> List[dict]:
        """Method to get list of tickers from polygon.io"""
        if not cls.__tickers:
            filters = cls.__configuration['gather']['data-source']['tickers']['filters']
            cls.__logger.info('loading all tickers from cache')
            cls.__tickers.extend(cls.__fetch_tickers(filters=filters))
        cls.__logger.info(f'number of available tickers: {len(cls.__tickers)}')
        return cls.__tickers

    @classmethod
    def get_ticker_overview_in_a_range(cls, ticker_symbols: List[str], start_date: str, end_date: str) -> List[dict]:
        """method to get list of ticker overviews  within a given date range from polygon.io """
        results = list()
        cls.__logger.info('obtaining tickers overview details in a given date range')
        overview_date_range = Commons.generate_date_range(start_date, end_date)
        for overview_date in overview_date_range:
            result = cls.get_ticker_overview_in_a_given_date(ticker_symbols, overview_date)
            results.extend(result)
        return results

    @classmethod
    def get_ticker_overview_in_a_given_date(cls, ticker_symbols: List[str], overview_date: str) -> List[dict]:
        """Method to get list of ticker overviews from polygon.io"""
        filters = cls.__configuration['gather']['data-source']['tickers']['filters']
        if not filters:
            filters = dict()
        filters.update({'date': overview_date})
        results = cls.__fetch_ticker_overviews(ticker_symbols=ticker_symbols, filters=filters)
        cls.__logger.info(f'number of available ticker overviews: {len(results)}')
        return results

    @classmethod
    def __fetch_ticker_overviews(cls, ticker_symbols:List[str], filters: dict = None) -> List[dict]:
        """Method to fetch ticker overviews api from polygon.io"""
        cls.__logger.info('fetching all tickers overview from source (polygon.io)')
        results = list()
        data_date = filters.get('date', date.today().strftime('%Y-%m-%d'))
        for ticker_symbol in ticker_symbols:
            result = cls.__fetch_one_ticker_overview(ticker_symbol=ticker_symbol, filters=filters)
            time.sleep(15)
            if result:
                result.update({'data_date': data_date})
                results.append(result)
        return results

    @classmethod
    def __fetch_one_ticker_overview(cls, ticker_symbol:str, filters:dict = None) -> Optional[dict]:
        """Method to fetch overview of a single ticker from polygon.io"""
        cls.__logger.info(f'fetching tickers overview of {ticker_symbol} from source (polygon.io)')
        result = None
        url = f'{cls.__tickers_overview_init_url}/{ticker_symbol}'
        params = Commons.build_params(filters=filters)
        try:
             response = Web.request(
                 method='GET',
                 url=url,
                 headers=None,
                 params=params,
                 body=None
             )
             result = response.get('results', None)
        except Exception as exception:
            cls.__logger.exception(exception)
        return result

    @classmethod
    def __fetch_tickers(cls, filters: dict = None) -> List[dict]:
        """Method to call tickers api from polygon.io (massive) sequentially"""
        cls.__logger.info('fetching tickers from source (polygon.io)')
        call_count = 1
        results = list()
        url = cls.__tickers_init_url
        params = Commons.build_params(filters=filters)
        try:
            while url:
                cls.__logger.info(f'making api call (count = {call_count}). url = {url}')
                response = Web.request(
                    method='GET',
                    url=url,
                    headers=None,
                    params=params,
                    body=None
                )
                if 'results' in response.keys():
                    cls.__logger.info(f"received objects in response: {len(response['results'])}")
                    results.extend(response['results'])
                if 'next_url' in response.keys():
                    call_count += 1
                    url = response['next_url']
                    time.sleep(15)
                else:
                    cls.__logger.info('next url not found. exiting sequential api call')
                    url = None
        except Exception as exception:
            cls.__logger.exception(exception)
        return results
