import random
import time
import traceback
from ib_insync import MarketOrder, Order, IB

from utils.trade_utils import (
cancel_all_pending_buy_orders, 
check_if_own_option, 
get_reversion,
sell_at_days_end
)

from utils.time_utils import (
sleep_until_market_open,
sleep_until_next_block,
time_until_market_close,
)

from utils.data_utils import (
    get_stock_sma_dict,
)


def setup_parameters():
    """
    Setup parameters for trading with Interactive Brokers.

    Returns:
    - ib (IB): Interactive Brokers (IB) API object connected to the trading server
    - acc_val (float): The current account balance in USD
    - block_size (int): The time block size for trading (in minutes)
    - perc_of_acct_to_trade (float): Percentage of account balance to trade
    - time_market_closes (int): The time when the market closes (in hours)
    - ticker_list (list of str): List of ticker symbols to trade
    """
    ib = IB()

    # Connect to paper or real trading servers
    # ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))  # For paper trading
    ib.connect('127.0.0.1', 7496, clientId=random.randint(0, 300))  # For live trading

    # Get the current account balance in USD.
    acc_val = float([v.value for v in ib.accountValues() if v.tag == 'CashBalance' and v.currency == 'USD'][0])

    # Set trading parameters
    block_size = 5  # Time block size (in minutes)
    perc_of_acct_to_trade = 0.5  # Percentage of account balance to trade
    time_market_closes = 16  # Time when market closes (in hours)
    ticker_list = ['SPY']  # List of tickers to trade

    return ib, acc_val, block_size, perc_of_acct_to_trade, time_market_closes, ticker_list 


def place_order(qty, contract, direction, block_size, avg_red, avg_green, ib):
    """
    Place an order to buy an option with a trailing stop.

    Args:
    - qty (int): Quantity of contracts to buy
    - contract (ib_insync.Contract): The option contract to buy
    - direction (str): Whether to go long or short on the option
    - block_size (int): The time block size (in minutes)
    - avg_red (float): Average value for red candles
    - avg_green (float): Average value for green candles
    - ib (IB): Interactive Brokers (IB) API object

    Returns:
    - qty (int): Quantity of contracts bought
    - mid (float): Mid price for the contract at the time of order placement
    """
    # Get contract data
    ib.qualifyContracts(contract)
    contract_data = ib.reqTickers(contract)[0]

    # Calculate delta, limit price, and delta_frac
    delta = abs(contract_data.lastGreeks.delta)
    mid = round((contract_data.bid + contract_data.ask) / 2, 2)

    # Calculate trailing percent based on delta, mid price and average red/green values
    delta_frac_multiplier = avg_red * 0.25 if direction == 'Long' else avg_green * 0.25
    delta_frac_base = (delta / mid) * 100
    delta_frac = round(delta_frac_base * delta_frac_multiplier, 2)

    # Create buy and sell orders
    buy_order = MarketOrder(action='BUY', totalQuantity=qty)
    sell_order = Order(action='SELL', totalQuantity=qty,
                       orderType='TRAIL', trailingPercent=delta_frac)
    sell_order.parentId = buy_order.orderId

    # Place the orders and wait for the buy order to be filled
    ib.placeOrder(contract, buy_order)
    while not check_if_own_option(ib):
        ib.sleep(0.25)

    # Place trailing stop sell order
    ib.placeOrder(contract, sell_order)

    # Wait for order to be filled and cancel all pending buy orders after given time
    time.sleep(block_size * 8)
    cancel_all_pending_buy_orders(ib)

    return qty, mid


def execute_trades(ib, acc_val, ticker_list, block_size, perc_of_acct_to_trade):
    """
    Execute trades for the current time block.

    Args:
    - ticker_list (list[str]): List of tickers to trade
    - block_size (int): The time block size (in minutes)
    - perc_of_acct_to_trade (float): Percentage of account balance to trade
    - ib (IB): Interactive Brokers (IB) API object

    Returns:
    - amount_traded (float): The total amount traded in this time block
    """
    # Get EMA and Connors RSI data
    avg_red, avg_green, stock_sma_dict = get_stock_sma_dict(
        ib, ticker_list, block_size)

    # Wait until the next time block
    sleep_until_next_block(block_size)

    # Get potential trade direction, qty, and contract
    direction, qty, contract = get_reversion(
        ib, acc_val, ticker_list, block_size, perc_of_acct_to_trade, stock_sma_dict)
    
    if not direction:
        print('No trades found')

    # Place order if there's enough time until market close
    if time_until_market_close(16) > (block_size * 60) and not check_if_own_option(ib):
        qty, mid = place_order(
            qty, contract, direction, block_size, avg_red, avg_green, ib)
        return qty * (mid * 100)

    return 0


def run_option_script():
    """
    Main trading loop.
    """

    # Setup trading parameters
    ib, acc_val, block_size, perc_of_acct_to_trade, time_market_closes, ticker_list = setup_parameters()

    # Initialize trading state
    amount_traded = 0
    max_amount_to_trade = acc_val - (acc_val * perc_of_acct_to_trade)

    # Wait for market open
    sleep_until_market_open()

    # Execute trades until market close or daily trade limit is reached
    while time_until_market_close(time_market_closes) > (block_size * 60) and amount_traded < max_amount_to_trade:
        try:
            amount_traded += execute_trades(ib, acc_val, ticker_list, block_size, perc_of_acct_to_trade)
            print(
                f'Total amount traded today: ${amount_traded:.2f}'
                f' ({amount_traded / acc_val * 100:.2f}% of account)\n'
            )
        except Exception as err:
            print(traceback.format_exc())

    # Cancel all existing orders and sell all positions at the end of the day
    if time_until_market_close(time_market_closes) < (block_size * 60):
        ib.reqGlobalCancel()
        sell_at_days_end(ib)
