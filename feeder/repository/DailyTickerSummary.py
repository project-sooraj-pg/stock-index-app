import asyncio
import json
from typing import List, Optional

from feeder.utility.Web import Web
from feeder.utility.Logger import Logger
from feeder.utility.Commons import Commons
from feeder.utility.Configuration import Configuration

class DailyTickerSummary:

    __logger = Logger.get_logger()
    __configuration = Configuration.load_from_file()
    __daily_ticker_summary_init_url = __configuration['gather']['data-source']['daily-ticker-summary']['url']

    @classmethod
    def get_price_data(cls, ticker_symbols: List[str], trade_date: str) -> List[dict]:
        """Method to get price data of tickers from polygon.io during a specific trade_date"""
        all_results = list()
        cls.__logger.info(f'requesting price data of multiple tickers. number of tickers: {len(ticker_symbols)}')
        filters = cls.__configuration['gather']['data-source']['tickers']['filters']
        batch_size = cls.__configuration['gather']['data-source']['tickers']['async-api-call-batch-size']
        batches = Commons.split_array_into_batches(ticker_symbols, batch_size=batch_size)
        for batch in batches:
            results = asyncio.run(cls.__fetch_price_data_by_trade_date(ticker_symbols=batch, trade_date=trade_date, filters=filters))
            all_results.extend(results)
        return all_results

    @classmethod
    async def __fetch_price_data_by_trade_date(cls, ticker_symbols: List[str], trade_date: str, filters: dict) -> List[dict]:
        """Method to submit asynchronous function calls"""
        tasks =  [cls.__fetch_price_data_by_ticker_symbol_trade_date(ticker_symbol, trade_date, filters) for ticker_symbol in ticker_symbols]
        results = await asyncio.gather(*tasks)
        return results

    @classmethod
    async def __fetch_price_data_by_ticker_symbol_trade_date(cls, ticker_symbol: str, trade_date: str, filters: dict = None) -> Optional[dict]:
        """Method to fetch price data of ticker on a specific date from polygon.io"""
        result = None
        params = Commons.build_params(filters)
        url = f'{cls.__daily_ticker_summary_init_url}/{ticker_symbol}/{trade_date}'
        try:
            response = await Web.request_asynchronous(
                method='GET',
                url=url,
                headers=None,
                params=params,
                body=None)
            response = json.loads(response)
            status = response.get('status', 'ERROR - status field not found in response')
            if status == 'OK':
                result = response
            else:
                cls.__logger.info(f'price data not found for ticker: {ticker_symbol} on date: {trade_date}')
        except Exception as exception:
            cls.__logger.exception(exception)
        return result
