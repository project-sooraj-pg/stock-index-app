from typing import List

from feeder.repository.Tickers import Tickers
from feeder.repository.DailyTickerSummary import DailyTickerSummary

from feeder.utility.Logger import Logger
from feeder.utility.DuckDB import DuckDB
from feeder.utility.Configuration import Configuration

class Gather:

    __logger = Logger.get_logger()
    __configuration = Configuration.load_from_file()

    @classmethod
    def gather_data(cls, override_previous:bool = True) -> None:
        """Method to gather all data into duckdb"""
        if override_previous:
            DuckDB.wipe_existing_data()
        try:
            tickers = Tickers.get_tickers()
            DuckDB.save_data(table_name='ticker', data=tickers)
            ticker_symbols = cls.__extract_ticker_symbols(tickers)
            ticker_details = Tickers.get_ticker_overview_in_a_range(ticker_symbols=ticker_symbols, start_date='', end_date='')
            DuckDB.save_data(table_name='ticker_detail', data=ticker_details)
            ticker_prices = DailyTickerSummary.get_price_data(ticker_symbols=ticker_symbols, start_date='', end_date='')
            DuckDB.save_data(table_name='ticker_price', data=ticker_prices)
        except Exception as exception:
            cls.__logger.exception(exception)

    @classmethod
    def __extract_ticker_symbols(cls, tickers: List[dict]) -> List[str]:
        """Method to extract ticker symbols from ticker objects"""
        ticker_symbols = set()
        for ticker in tickers:
            ticker_symbol = ticker.get('ticker', None)
            if ticker_symbol:
                ticker_symbols.add(ticker_symbol)
        return list(ticker_symbols)