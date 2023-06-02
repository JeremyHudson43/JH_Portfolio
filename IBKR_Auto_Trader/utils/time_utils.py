from datetime import datetime
import time

def sleep_until_market_open():
    """
    Sleeps the program until the market next opens at 9:40 AM EST.

    Calculates the time remaining until the market opens and sleeps for that duration.
    """
    time_now = datetime.now()
    market_open = time_now.replace(hour=9, minute=40, second=0, microsecond=0)

    time_until_market_opens = market_open - time_now
    seconds_until_market_opens = time_until_market_opens.total_seconds()

    if seconds_until_market_opens > 0:
        hours, remainder = divmod(time_until_market_opens.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if seconds > 0:
            minutes += 1

        print(f'\nSleeping for {hours} hours and {minutes} minute(s) until 9:40 AM EST')
        time.sleep(seconds_until_market_opens)


def sleep_until_next_block(block_size):
    """
    Sleeps the program until the next trading block.

    Args:
        block_size: An integer representing the size of the trading block in minutes.

    Calculates the time remaining until the next trading block starts and sleeps for that duration.
    """
    current_time = datetime.now()

    next_block_minute = (current_time.minute // block_size + 1) * block_size
    next_block_hour = current_time.hour

    if next_block_minute == 60:
        next_block_hour += 1
        next_block_minute = 0

    next_block_time = current_time.replace(hour=next_block_hour, minute=next_block_minute, second=0, microsecond=0)
    seconds_left = (next_block_time - current_time).total_seconds() + 0.1

    minutes, seconds = divmod(seconds_left, 60)
    minutes, seconds = round(minutes), round(seconds)

    print(f'\nSleeping for {minutes} minutes and {seconds} seconds until the next candle')
    print('------------------------------------------------------------')

    if seconds_left > 0:
        time.sleep(seconds_left)


def time_until_market_close(close_time):
    """
    Calculates and returns the time until the market closes in seconds.

    Args:
        close_time: An integer representing the hour (in 24 hour format) when the market closes.

    Returns:
        seconds_until_market_close: An integer representing the number of seconds until the market closes.
    """
    time_now = datetime.now()
    end_time = time_now.replace(hour=close_time, minute=0, second=0, microsecond=0)

    time_difference = end_time - time_now
    seconds_until_market_close = time_difference.total_seconds()

    return seconds_until_market_close