from typing import List, Optional

from feeder.repository.Tickers import Tickers
from feeder.repository.DailyTickerSummary import DailyTickerSummary
from feeder.utility.Commons import Commons

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
            start_date = cls.__configuration['gather']['start_date']
            end_date = cls.__configuration['gather']['end_date']
            tickers = Tickers.get_tickers()
            DuckDB.save_data(table_name='ticker', data=tickers)
            ticker_symbols = cls.__extract_ticker_symbols(tickers)
            trade_date_range = Commons.generate_date_range(start_date, end_date)
            batch_size = cls.__configuration['gather']['persistence-batch-size']
            batches = Commons.split_array_into_batches(trade_date_range, batch_size=batch_size)
            for batch in batches:
                cls.__gather_ticker_overview_by_trade_date_batches(ticker_symbols=ticker_symbols, trade_dates=batch)
                cls.__gather_price_data_by_trade_date_batches(ticker_symbols=ticker_symbols, trade_dates=batch)
            DuckDB.close_connection()
        except Exception as exception:
            cls.__logger.exception(exception)

    @classmethod
    def __gather_ticker_overview_by_trade_date_batches(cls, ticker_symbols: List[str], trade_dates: List[str]) -> None:
        """Method to gather ticker overview data during a batch of trade dates"""
        try:
            results = list()
            for trade_date in trade_dates:
                ticker_details = Tickers.get_ticker_overview_in_a_given_date(ticker_symbols=ticker_symbols, overview_date=trade_date)
                results.extend(ticker_details)
            DuckDB.save_data('ticker_overview', results)
        except Exception as exception:
            cls.__logger.exception(exception)

    @classmethod
    def __gather_price_data_by_trade_date_batches(cls, ticker_symbols: List[str], trade_dates: List[str]) -> None:
        """Method to gather price data during a batch of trade dates"""
        try:
            results = list()
            for trade_date in trade_dates:
                ticker_prices = DailyTickerSummary.get_price_data(ticker_symbols=ticker_symbols, trade_date=trade_date)
                results.extend(ticker_prices)
            DuckDB.save_data(table_name='ticker_price', data=results)
        except Exception as exception:
            cls.__logger.exception(exception)

    @classmethod
    def __extract_ticker_symbols(cls, tickers: List[dict]) -> List[Optional[str]]:
        """Method to extract ticker symbols from ticker objects"""
        cls.__logger.info('extracting ticker symbols from ticker data')
        ticker_symbols = set()
        for ticker in tickers:
            ticker_symbol = ticker.get('ticker', None)
            if ticker_symbol:
                ticker_symbols.add(ticker_symbol)
        cls.__logger.info(f'extracted: number of ticker symbols: {len(ticker_symbols)}')
        return list(ticker_symbols)