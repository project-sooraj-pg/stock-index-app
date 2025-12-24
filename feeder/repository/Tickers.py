import json
import asyncio
from datetime import  date
from typing import List, Optional

from utility.Web import Web
from utility.Logger import Logger
from utility.Commons import Commons
from utility.Configuration import Configuration

class Tickers:

    __logger = Logger.get_logger()
    __configuration = Configuration.load_from_file()
    __tickers_init_url = __configuration['gather']['data-source']['tickers']['url']
    __tickers_overview_init_url = __configuration['gather']['data-source']['ticker-overview']['url']

    @classmethod
    def get_tickers(cls) -> List[dict]:
        """Method to get list of tickers from polygon.io"""
        filters = cls.__configuration['gather']['data-source']['tickers']['filters']
        tickers = cls.__fetch_tickers(filters=filters)
        cls.__logger.info(f'number of available tickers: {len(tickers)}')
        return tickers

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
    def __fetch_ticker_overviews(cls, ticker_symbols:List[str], filters: dict = None) -> List[Optional[dict]]:
        """Method to fetch ticker overviews api from polygon.io"""
        cls.__logger.info('fetching all tickers overview from source (polygon.io)')
        ticker_overviews = list()
        data_date = filters.get('date', date.today().strftime('%Y-%m-%d'))
        batch_size = cls.__configuration['gather']['data-source']['ticker-overview']['async-api-call-batch-size']
        batches = Commons.split_array_into_batches(ticker_symbols, batch_size=batch_size)
        for batch in batches:
            cls.__logger.info(f"processing ticker symbol batch of size: {len(batch)}")
            results = asyncio.run(cls.__fetch_batch_ticker_overview(batch, filters))
            for result in results:
                if result:
                    result.update({'data_date': data_date})
            ticker_overviews.extend(results)
        return ticker_overviews

    @classmethod
    async def __fetch_batch_ticker_overview(cls, ticker_symbols: List[str], filters: dict) -> List[dict]:
        """Method to submit asynchronous function calls"""
        tasks = [cls.__fetch_one_ticker_overview(ticker_symbol, filters) for ticker_symbol in ticker_symbols]
        results = await asyncio.gather(*tasks)
        return results

    @classmethod
    async def __fetch_one_ticker_overview(cls, ticker_symbol:str, filters:dict = None) -> Optional[dict]:
        """Method to fetch overview of a single ticker from polygon.io"""
        result = None
        url = f'{cls.__tickers_overview_init_url}/{ticker_symbol}'
        params = Commons.build_params(filters=filters)
        try:
             response = await Web.request_asynchronous(
                 method='GET',
                 url=url,
                 headers=None,
                 params=params,
                 body=None
             )
             response = json.loads(response)
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
                else:
                    cls.__logger.info('next url not found. exiting sequential api call')
                    url = None
        except Exception as exception:
            cls.__logger.exception(exception)
        return results
