import traceback
from datetime import date
from ib_insync import Stock
import time
from math import floor

from utils.data_utils import (
    get_latest_close,
)   


def check_gap(open_price, prev_close_price):
    """
    Check if there is a gap up or down in the stock price.

    :param open_price: The stock's open price.
    :param prev_close_price: The stock's previous close price.
    :return: A tuple containing two boolean values indicating if there is a gap up or down.
    """
    gap_up = open_price > prev_close_price * 1.05
    gap_down = open_price < prev_close_price * 0.95

    return gap_up, gap_down

def calculate_order_prices(open_price, avg_red, avg_green):
    """
    Calculate the limit price, stop price, and take profit price for the stock order.

    :param open_price: The stock's open price.
    :param avg_red: The average red candle size.
    :param avg_green: The average green candle size.
    :return: A tuple containing the limit price, stop price, and take profit price.
    """
    limit_price = open_price - avg_red

    if limit_price < open_price * 0.98:
        limit_price = open_price * 0.98

    stop_price = limit_price - (avg_red * 3)

    if stop_price < limit_price * 0.98:
        stop_price = limit_price * 0.98

    take_profit = limit_price + avg_green

    limit_price = round(limit_price, 2)
    stop_price = round(stop_price, 2)
    take_profit = round(take_profit, 2)

    return limit_price, stop_price, take_profit

def place_bracket_order(ib, stock_contract, quantity, limit_price, take_profit, stop_price):
    """
    Place a bracket order for the stock with take profit and stop loss orders.

    :param stock_contract: The stock contract object.
    :param quantity: The number of shares to buy.
    :param limit_price: The limit price for the stock order.
    :param take_profit: The take profit price for the stock order.
    :param stop_price: The stop loss price for the stock order.
    """
    buy_order = ib.bracketOrder(
        'BUY',
        quantity=quantity,
        limitPrice=limit_price,
        takeProfitPrice=take_profit,
        stopLossPrice=stop_price
    )

    for o in buy_order:
        o.tif = 'GTC'
        ib.sleep(0.00001)
        ib.placeOrder(stock_contract, o)

def buy_stock(ib, ticker, long_length, exchange):
    """
    Buy the stock with a bracket order and place take profit and stop loss orders.

    :param ticker: The stock ticker symbol.
    :param long_length: The number of long positions to take.
    :param exchange: The stock exchange.
    """
    try:
        stock_contract = Stock(symbol=ticker, exchange=exchange, currency='USD')
        ib.qualifyContracts(stock_contract)

        while True:
            stock_df, exchange, avg_red, avg_green = get_latest_close(ib, ticker)

            if stock_df is None:
                break

            latest_date = stock_df['date'].iloc[-1]

            if latest_date == date.today():
                break

            time.sleep(1)

        close = stock_df['close']
        open = stock_df['open']

        prev_close_price = close.iloc[-2]
        open_price = open.iloc[-1]

        gap_up, gap_down = check_gap(open_price, prev_close_price)

        if not gap_up and not gap_down:
            limit_price, stop_price, take_profit = calculate_order_prices(open_price, avg_red, avg_green)

            settled_cash = get_settled_cash(ib)

            quantity = (settled_cash // open_price) * (1 / long_length)
            quantity = floor(quantity)

            place_bracket_order(stock_contract, quantity, limit_price, take_profit, stop_price)

        print(f'\nPlaced order for {ticker} stock')

    except Exception as err:
        print(traceback.format_exc())

