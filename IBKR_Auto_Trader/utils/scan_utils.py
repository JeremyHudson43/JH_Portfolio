import talib
from finviz.screener import Screener
from helper_functions import get_latest_close
import traceback
import time
from connors_rsi import ConnorsRSI


def calculate_crsi(stock_df, num):
    """
    Calculate the Connors RSI (CRSI) for a given stock DataFrame.
    
    Args:
        stock_df: DataFrame containing stock data.
        num: Number of days.
        
    Returns:
        crsi: Connors RSI value for the stock DataFrame.
    """
    crsi_obj = ConnorsRSI(stock_df, 3, 2, 100)
    crsi = crsi_obj.calc_connors_rsi().iloc[-num]

    return crsi


def calculate_adx(stock_df, high, low, num):
    """
    Calculate the ADX for a given stock DataFrame.
    
    Args:
        stock_df: DataFrame containing stock data.
        high: Series containing the high prices.
        low: Series containing the low prices.
        num: Number of days.
        
    Returns:
        adx_10: ADX value for the stock DataFrame.
    """
    stock_df['10_ADX'] = talib.ADX(high, low, timeperiod=10)
    adx_10 = stock_df['10_ADX'].iloc[-num]

    return adx_10


def calculate_ema(stock_df, close):
    """
    Calculate the 100 EMA for a given stock DataFrame.
    
    Args:
        stock_df: DataFrame containing stock data.
        close: Series containing the closing prices.
        
    Returns:
        hundred_ema: 100 EMA value for the stock DataFrame.
    """
    stock_df['100_EMA'] = talib.EMA(close, timeperiod=100)
    hundred_ema = stock_df['100_EMA'].iloc[-1]

    return hundred_ema


def is_stock_long(high, low, close, num):
    """
    Determine if a stock meets the long conditions.
    
    Args:
        high: Series containing the high prices.
        low: Series containing the low prices.
        close: Series containing the closing prices.
        num: Number of days.
        
    Returns:
        is_long: Boolean indicating if the stock meets the long conditions.
    """
    last_close = close.iloc[-num]
    last_low = low.iloc[-num]
    last_high = high.iloc[-num]

    close_minus_low = last_close - last_low
    high_minus_low = last_high - last_low

    close_long = (low.iloc[-num] / close.iloc[-num - 1]) < 0.98
    close_range = (close_minus_low / high_minus_low) < 0.25

    return close_long and close_range


def check_indicator_match(stock_df, high, low, close, ticker, num, exchange_return):
    """
    Get a list of long stocks based on specific conditions.
    
    Args:
        stock_df: DataFrame containing stock data.
        high: Series containing the high prices.
        low: Series containing the low prices.
        close: Series containing the closing prices.
        ticker: The stock ticker symbol.
        num: Number of days.
        exchange_return: The stock exchange return.
        
    Returns:
        long_stock_list: List of tuples with long stocks that meet the conditions.
    """
    long_stock_list = []

    crsi = calculate_crsi(stock_df, num)
    adx_10 = calculate_adx(stock_df, high, low, num)
    hundred_ema = calculate_ema(stock_df, close)

    close_long = is_stock_long(high, low, close, num)
    above_all_ema = close.iloc[-num] > hundred_ema

    if crsi <= 8 and adx_10 > 30 and close_long and above_all_ema:
        long_stock_list.append((ticker, crsi, exchange_return))
        print(ticker, crsi, exchange_return)

    return long_stock_list


def scan_finviz_stocks():
    """
    Get a list of stocks from Finviz using specific filters.
    
    Returns:
        finviz_ticker_list: List of stock ticker symbols that pass the filter conditions.
    """
    filters = ['sh_avgvol_o300', 'sh_price_o5', 'ipodate_more1']
    finviz_stock_list = Screener(filters=filters, table='Performance', order='price')
    finviz_ticker_list = [stock['Ticker'] for stock in finviz_stock_list]

    time.sleep(10)

    earnings_soon = ['earningsdate_nextdays5']
    earnings_stock_list = Screener(filters=earnings_soon, table='Performance', order='price')
    earnings_ticker_list = [stock['Ticker'] for stock in earnings_stock_list]

    # remove all stocks that are in the earnings list in a list comprehension
    finviz_ticker_list = [stock for stock in finviz_ticker_list if stock not in earnings_ticker_list]
    
    return finviz_ticker_list


def filter_stocks(ib, finviz_ticker_list):
    """
    Filter stocks based on specific conditions and return a list of long stocks.
    
    Args:
        finviz_ticker_list: List of stock ticker symbols that pass the filter conditions.
        
    Returns:
        sorted_long_list: List of tuples with long stocks that meet the conditions.
    """
    long_stock_list = []

    for ticker in finviz_ticker_list:

        try:

            ib.sleep(0.2)

            stock_df, exchange, _, _ = get_latest_close(ib, ticker)
            high, low, close = stock_df['high'], stock_df['low'], stock_df['close']

            num = 1

            long_stocks = check_indicator_match(stock_df, high, low, close, ticker, num, exchange)
            long_stock_list.extend(long_stocks)

        except Exception as err:
            print(traceback.format_exc())

    # take 3 lowest crsi stocks and return them
    sorted_long_list = sorted(long_stock_list, key=lambda x: x[1])[:3]

    return sorted_long_list