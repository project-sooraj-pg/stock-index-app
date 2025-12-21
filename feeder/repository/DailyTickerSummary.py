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
    def get_price_data(cls, ticker_symbols: List[str], start_date: str, end_date: str) -> List[dict]:
        """Method to get price data of tickers from polygon.io during a specific date range"""
        all_results = list()
        cls.__logger(f'requesting price data of multiple tickers. number of tickers: {len(ticker_symbols)}')
        for ticker_symbol in ticker_symbols:
            filters = cls.__configuration['gather']['data-source']['tickers']['filters']
            results = cls.get_price_data_by_ticker(ticker_symbol, start_date, end_date, filters)
            all_results.extend(results)
        return all_results

    @classmethod
    def get_price_data_by_ticker(cls, ticker_symbol: str, start_date: str, end_date: str, filters: dict = None) -> List[dict]:
        """Method to get price data of ticker from polygon.io during a specific date range"""
        results = list()
        cls.__logger(f'requesting price data for ticker: {ticker_symbol}')
        trade_date_range = Commons.generate_date_range(start_date=start_date, end_date=end_date)
        for trade_date in trade_date_range:
            result = cls.__fetch_price_data_by_ticker_symbol_trade_date(ticker_symbol, trade_date, filters)
            if result:
                results.append(result)
        return results

    @classmethod
    def __fetch_price_data_by_ticker_symbol_trade_date(cls, ticker_symbol: str, trade_date: str, filters: dict = None) -> Optional[dict]:
        """Method to fetch price data of ticker on a specific date from polygon.io"""
        result = None
        params = Commons.build_params(filters)
        url = f'{cls.__daily_ticker_summary_init_url}/{ticker_symbol}/{trade_date}'
        try:
            response = Web.request(
                method='GET',
                url=url,
                headers=None,
                params=params,
                body=None)
            status = response.get('status', 'ERROR - status field not found in response')
            if status == 'OK':
                result = response
            else:
                cls.__logger.info(f'price data not found for ticker: {ticker_symbol} on date: {trade_date}')
        except Exception as exception:
            cls.__logger.exception(exception)
        return result
