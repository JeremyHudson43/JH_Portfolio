import pandas as pd
from datetime import datetime
from ib_insync import Stock

def get_settled_cash(ib):
    account_summary = ib.accountSummary()

    for account_value in account_summary:
        if account_value.tag == "CashBalance":
            settled_cash = account_value.value

    settled_cash = float(settled_cash)
    settled_cash = settled_cash * 0.15
    settled_cash = round(settled_cash, 2)

    print(f'Settled cash: ${settled_cash}')

    return settled_cash


def get_latest_close(ib, ticker, block_size):
    """
    Fetches the historical data with the latest close prices for a given stock ticker.
    
    Args:
    ib (IB): The instance of ib_insync's IB class
    ticker (str): The stock ticker symbol
    block_size (int): The time interval in minutes for each bar

    Returns:
    pd.DataFrame: A dataframe containing historical data with the latest close prices
    """
    current_time = datetime.now()
    current_minute = current_time.minute

    previous_block_minute = (current_minute // block_size) * block_size
    previous_block_time = current_time.replace(minute=previous_block_minute, second=0, microsecond=0)

    # Set the reference time to 9:30 AM
    reference_time = datetime(current_time.year, current_time.month, current_time.day, 9, 30)

    difference = (current_time - reference_time).total_seconds() + 60
    difference = int(difference)

    if block_size == 1:
        bar_size = '1 min'
    else:
        bar_size = f'{block_size} mins'

    stock_df = pd.DataFrame(
        ib.reqHistoricalData(
            Stock(ticker, 'SMART', 'USD'),
            endDateTime=previous_block_time,
            durationStr=f'{difference} S',
            barSizeSetting=bar_size,
            whatToShow="TRADES",
            useRTH=True,
            formatDate=1))

    stock_df = stock_df.dropna()

    return stock_df


def get_average_bar_size(bars):
    """
    Computes the average bar size for green and red candles.

    Args:
    bars (List[BarData]): A list of bar data objects

    Returns:
    Tuple[float, float]: The average red candle size and the average green candle size
    """
    green_differences = []
    red_differences = []

    for bar in bars:
        # green candle
        if bar.open < bar.close:
            green_differences.append(bar.close - bar.open)
        # red candle
        else:
            red_differences.append(bar.open - bar.close)

    avg_green = sum(green_differences) / len(green_differences)
    avg_red = sum(red_differences) / len(red_differences)

    return avg_red, avg_green


def get_stock_sma_dict(ib, ticker_list, block_size):
    """
    Fetches the historical data for the past (block_size * 3) days for a list of stock tickers.

    Args:
    ib (IB): The instance of ib_insync's IB class
    ticker_list (List[str]): A list of stock ticker symbols
    block_size (int): The time interval in minutes for each bar

    Returns:
    Tuple[float, float, Dict[str, pd.DataFrame]]: The average red candle size, the average green candle size, and a 
    dictionary whose keys are stock tickers and values are the corresponding dataframes containing historical data
    """
    stock_sma_dict = {}

    today = datetime.today()
    today_nine_thirty = today.replace(hour=9, minute=30, second=0, microsecond=0)

    for ticker in ticker_list:

        if block_size == 1:
            bar_size = '1 min'
        else:
            bar_size = f'{block_size} mins'

        bars = ib.reqHistoricalData(
            Stock(ticker, 'SMART', 'USD'),
            endDateTime=today_nine_thirty,
            durationStr=f'{block_size * 3} D',
            barSizeSetting=bar_size,
            whatToShow="TRADES",
            useRTH=True,
            formatDate=1)

        avg_red, avg_green = get_average_bar_size(bars)

        stock_df = pd.DataFrame(bars)
        stock_sma_dict[ticker] = stock_df

        ib.sleep(1)

        # print(f'\nFinished {ticker} download')

    return avg_red, avg_green, stock_sma_dict


def get_vwap(ib, stock, block_size):
    """
    Calculates the Volume Weighted Average Price (VWAP) for a stock.

    Args:
    ib (IB): The instance of ib_insync's IB class
    stock (str): The stock ticker symbol
    block_size (int): The time interval in minutes for each bar

    Returns:
    float: The calculated VWAP for the stock
    """
    stock_df = get_latest_close(ib, stock, block_size)

    # drop any rows with date not equal to today
    stock_df = stock_df[stock_df.date >= datetime.today().strftime('%Y%m%d')]

    high, low, close = stock_df['high'], stock_df['low'], stock_df['close']
    avg_price = (high + low + close) / 3

    stock_df['vwap'] = (avg_price * stock_df['volume']).cumsum() / stock_df['volume'].cumsum()

    return stock_df['vwap'].iloc[-1]


def append_latest_close(ib, stock_df, block_size, stock_sma_df):
    """
    Appends the latest close prices to the given stock_sma_df.

    Args:
    ib (IB): The instance of ib_insync's IB class
    stock_df (pd.DataFrame): A dataframe containing historical stock data
    block_size (int): The time interval in minutes for each bar
    stock_sma_df (pd.DataFrame): A dataframe containing the historical stock data along with SMA data

    Returns:
    pd.DataFrame: A dataframe containing the combined historical stock data and SMA data along with the latest close prices
    """
    latest_close_df = get_latest_close(ib, stock_df, block_size)

    combined_data = pd.concat([stock_sma_df, latest_close_df], axis=0)
    combined_data = combined_data.drop_duplicates(subset='date', keep='first')

    return combined_data

