import random
import time
from ib_insync import IB

from utils.buy_utils import (
    buy_stock,
    sell_stock_at_days_end,
)

from utils.time_utils import (
    sleep_until_market_open,
    time_until_market_close,
)

from utils.scan_utils import (
    scan_finviz_stocks,
    filter_stocks
)


def buy_and_sell_stocks(ib, long_stocks, num_long_stocks, action):
    """
    Buys or sells the stocks based on the action provided.

    Args:
        ib (IB): Interactive Brokers API object.
        long_stocks (list): List of long stocks (stock to trade).
        num_long_stocks (int): Number of long stocks.
        action (str): 'buy' or 'sell' to perform the corresponding action on the stocks.
    """
    for stock in long_stocks:
        ticker, _, exchange = stock
        if action == 'buy':
            buy_stock(ib, ticker, num_long_stocks, exchange)
        elif action == 'sell':
            sell_stock_at_days_end(ib, ticker, exchange)


def sleep_until_market_actions(sleep_time, action):
    """
    Sleeps until specific market action (buying or selling stocks).
    
    Args:
        sleep_time (int): Time to sleep in seconds.
        action (str): 'buy' or 'sell' to indicate which action is being performed.
    """
    if sleep_time > 0:
        print(f"Waiting for market to {action} stocks...")
        time.sleep(sleep_time)

def trade_stocks(ib, market_close_time):
    """
    Executes the trading operations for the day,
    and returns the list of long stocks.

    Args:
        ib (IB): Interactive Brokers API object.
        market_obj (scan_whole_market): Market scanner object.
        market_close_time (int): Time market closes in military time.

    Returns:
        long_stocks (list): List of long stocks (stock to trade).
    """
    long_stocks = scan_finviz_stocks()
    long_stocks = filter_stocks(ib, long_stocks)

    if not long_stocks:
        print("No stocks to trade today")
        return

    num_long_stocks = len(long_stocks)
    
    # Sleep until market opens and then buy stocks
    time_to_sleep = sleep_until_market_open()
    sleep_until_market_actions(time_to_sleep, 'buy')
    
    buy_and_sell_stocks(ib, long_stocks, num_long_stocks, 'buy')

    # Sleep until market closes and then sell stocks
    time_to_wait = time_until_market_close(market_close_time)
    sleep_until_market_actions(time_to_wait, 'sell')

    # Cancel all outstanding orders
    ib.sleep(1)
    ib.reqGlobalCancel()

    buy_and_sell_stocks(ib, long_stocks, num_long_stocks, 'sell')


def run_stock_script():
    """
    The main function to be executed.
    """
    market_close_time = 16  # Time market closes in military time

    # Connect to IB API
    ib = IB()
    ib.connect('127.0.0.1', 7496, clientId=random.randint(0, 300))  # For real trading

    # Get list of stocks for long trades and execute trades
    trade_stocks(ib, market_close_time)
