from ib_insync import Option, MarketOrder
from math import ceil, floor
from datetime import datetime, timedelta
import numpy as np
import traceback
from utils.data_utils import append_latest_close
from connors_rsi import ConnorsRSI

from utils.data_utils import get_vwap


def cancel_all_pending_buy_orders(ib):
    """
    Cancel all pending BUY orders.

    Args:
        ib (IB): An instantiated Interactive Brokers client.

    Returns:
        None
    """
    for order in ib.reqAllOpenOrders():
        if order.action == 'BUY':
            ib.cancelOrder(order)


def sell_at_days_end(ib):
    """
    Sell all options in the account at market price, if there are any.

    Args:
        ib (IB): An instantiated Interactive Brokers client.

    Returns:
        None
    """
    positions = ib.positions()

    if not positions:
        print('\nNo positions found\n')
        return

    for position in positions:

        if position.contract.secType != 'OPT':
            continue

        symbol = position.contract.symbol
        expiration_date = position.contract.lastTradeDateOrContractMonth
        right = position.contract.right
        strike = position.contract.strike
        quantity = position.position

        if quantity <= 0:
            continue

        option_contract = Option(symbol, expiration_date, strike, right, "SMART")
        print(f'\nAttempting to sell {symbol} option at market price')

        try:
            ib.qualifyContracts(option_contract)
            order = MarketOrder('SELL', totalQuantity=quantity)
            ib.placeOrder(option_contract, order)
        except Exception as err:
            print(err)


def get_new_strike(acc_vals, right, strike, mid, qty, ticker, percent_of_acct_to_trade):
    """
    Get a new strike price if the previous strike price did not fit the given account limits.

    Args:
        acc_vals (float): Account value.
        right (str): Call ('C') or Put ('P') option.
        strike (float): Strike price.
        mid (float): Mid point between bid and ask prices.
        qty (int): Quantity of options to trade.
        ticker (str): Ticker symbol.
        percent_of_acct_to_trade (float): The limit to trade percent.

    Returns:
        Tuple (str, bool): Updated strike price and a boolean indication whether the total_trade_cost is less than or equal to the max_trade_cost.
    """
    total_trade_cost = (mid * 100) * qty
    max_trade_cost = acc_vals * percent_of_acct_to_trade

    if total_trade_cost > max_trade_cost:

        if right == 'C':

            print(f'\n{ticker} {strike} call option too big for account, trying a different strike price\n')
            strike = int(strike) + 1

            return str(strike), False

        elif right == 'P':

            print(f'\n{ticker} {strike} put option too big for account, trying a different strike price\n')
            strike = int(strike) - 1

            return str(strike), False

    else:
        return strike, True


def check_spread_and_mid(mid, spread_perc):
    """
    Check if the spread and mid are within acceptable limits.

    Args:
        mid (float): Mid point between bid and ask prices.
        spread_perc (float): Percentage of spread between bid and ask prices.

    Returns:
        bool: True if mid and spread are within limits, False otherwise.
    """
    mid_limit = 0.75
    spread_limit = 3

    spread_perc = round(spread_perc, 2)
    mid = round(mid, 2)

    if mid < mid_limit or spread_perc > spread_limit:

        if mid < mid_limit:
            print(f'\nMid is too small: ${mid}')

        if spread_perc > spread_limit:
            print(f'\nSpread is too large: {spread_perc}%')

        return False

    return True


def get_order_details(ib, acc_vals, ticker, exp_date, strike, right, perc_of_acct_to_trade):
    """
    Get details of an option order (strike, qty, contract, mid) by attempting to qualify the contract for a given number of times.

    Args:
        ib (IB): An instantiated Interactive Brokers client.
        acc_vals (float): Account value.
        ticker (str): Ticker symbol of the stock.
        exp_date (str): Expiration date of the option.
        strike (float): Strike price.
        right (str): Call ('C') or Put ('P') option.
        perc_of_acct_to_trade (float): The limit to trade percent.

    Returns:
        Tuple (str, int, object, float): strike, qty, contract, mid
    """
    for attempts in range(5):

        contract = Option(ticker, exp_date, strike, right, "SMART")

        ib.qualifyContracts(contract)
        contract_data = ib.reqTickers(contract)[0]

        bid = contract_data.bid
        ask = contract_data.ask

        # if bid is NaN, increment exp_date by 1 day and try again
        if np.isnan(bid):
            exp_date = datetime.strptime(exp_date, '%Y%m%d').date() + timedelta(days=1)
            exp_date = exp_date.strftime('%Y%m%d')
            continue

        mid = (bid + ask) / 2
        mid_times_100 = mid * 100

        qty = (acc_vals // mid_times_100) * perc_of_acct_to_trade
        qty = floor(qty)

        if qty == 0:
            qty = 1

        spread_perc = (ask - bid) / bid
        spread_perc = spread_perc * 100

        strike, strike_fit = get_new_strike(acc_vals, right, strike, mid, qty, ticker, perc_of_acct_to_trade)
        spread_and_mid = check_spread_and_mid(mid, spread_perc)

        if strike_fit and spread_and_mid:
            return strike, qty, contract, mid

    return None, None, None, None


def get_exp_date():
    """
    Get the expiration date of an option with at least 1 day to expiration

    Returns:
        str: Expiration date as a string in the format 'YYYMMDD' 
    """
    today = datetime.today()

    days_to_add = {
        0: 2,  # Monday
        1: 1,  # Tuesday
        2: 2,  # Wednesday
        3: 1,  # Thursday
        4:3,  # Friday
    }

    exp_date = today + timedelta(days=days_to_add[today.weekday()])
    year, month, day = exp_date.year, exp_date.month, exp_date.day

    # add padding zeroes to the month and day if necessary
    exp_date = f"{year}{month:02}{day:02}"

    return exp_date


def check_if_own_option(ib):
    """
    Check if the account owns any options.

    Args:
        ib (IB): An instantiated Interactive Brokers client.

    Returns:
        bool: True if the account has options, False otherwise.
    """
    positions = ib.positions()
    own_option = any([position.contract.secType == 'OPT' for position in positions])

    return own_option


def get_reversion_helper(ib, acc_vals, ticker, last_price, right, perc_of_acct_to_trade):
    """
    Attempt to place an option order when the reversion conditions are met.

    Args:
        ib (IB): An instantiated Interactive Brokers client.
        acc_vals (float): Account value.
        ticker (str): Ticker symbol of the stock.
        last_price (float): Last price of the stock.
        right (str): Call ('C') or Put ('P') option.
        perc_of_acct_to_trade (float): The limit to trade percent.

    Returns:
        Tuple (str, int, object): Direction {'Long', 'Short'}, quantity, and contract object if conditions met, otherwise (None, None, None).
    """
    exp_date = get_exp_date()

    call_price = ceil(last_price)
    put_price = floor(last_price)

    if right == 'C':
        strike, qty, contract, mid = get_order_details(ib, acc_vals, ticker, exp_date, call_price, 'C', perc_of_acct_to_trade)

    elif right == 'P':
        strike, qty, contract, mid = get_order_details(ib, acc_vals, ticker, exp_date, put_price, 'P', perc_of_acct_to_trade)

    if strike is not None:

        if right == 'C':

            print(f'\nPlacing order for {qty} {ticker} call contract(s) at strike '
                    f'${strike} with a midpoint of ${round(mid, 2)}')

            return 'Long', qty, contract

        elif right == 'P':

            print(f'\nPlacing order for {qty} {ticker} put contract(s) at strike '
                    f'${strike} with a midpoint of ${round(mid, 2)}')

            return 'Short', qty, contract

    else:
        return None, None, None


def get_reversion(ib, acc_vals, ticker_list, block_size, perc_of_acct_to_trade, stock_sma_dict):
    """
    Determine the reversion trade conditions for each ticker in the list and return the order details if all conditions are met.

    Args:
        ib (IB): An instantiated Interactive Brokers client.
        acc_vals (float): Account value.
        ticker_list (list): List of ticker symbols.
        block_size (int): Block size required for VWAP and SMA calculations
        perc_of_acct_to_trade (float): The limit to trade percent.
        stock_sma_dict (dict): Dictionary containing stock dataframes with SMA values.

    Returns:
        Tuple (str, int, object): Direction {'Long', 'Short'}, quantity, and contract object if conditions met, otherwise (None, None, None).
    """
    for ticker in ticker_list:

        try:

            stock_df = append_latest_close(ib, ticker, block_size, stock_sma_dict[ticker])
            stock_close = stock_df['close']

            crsi = ConnorsRSI(stock_df, 3, 2, 100)
            crsi = crsi.calc_connors_rsi().iloc[-1]
            crsi = round(crsi)

            vwap = get_vwap(ib, ticker, block_size)
            last_price = stock_close.iloc[-1]

            above_vwap = last_price > (vwap * 1.001)
            below_vwap = last_price < (vwap * 0.999)

            print('Ticker:', ticker)
            print('Last Price:', last_price)
            print('Current Time:', datetime.now().strftime("%H:%M:%S"))
            print('Connors RSI:', round(crsi, 2))
            print('VWAP:', round(vwap, 2))

            if crsi < 25 and above_vwap:
                direction, qty, contract = get_reversion_helper(ib, acc_vals, ticker, last_price, 'C', perc_of_acct_to_trade)

                if direction is not None:
                    return direction, qty, contract

            elif crsi > 75 and below_vwap:
                direction, qty, contract = get_reversion_helper(ib, acc_vals, ticker, last_price, 'P', perc_of_acct_to_trade)

                if direction is not None:
                    return direction, qty, contract

        except Exception as err:
            print(traceback.format_exc())

        print('------------------------------------------------------------')

    return None, None, None