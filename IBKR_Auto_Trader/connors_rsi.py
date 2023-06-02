import pandas as pd
import numpy as np
import talib as ta

class ConnorsRSI:

    def __init__(self, stock_df, rsi_len, streak_len, percent_rank_len):
        self.stock_df = stock_df
        self.rsi_len = rsi_len
        self.streak_len = streak_len
        self.percent_rank_len = percent_rank_len

    def streaks(self, stock_prices):
        """
        This function identifies 'streaks' or consecutive increases or decreases in stock prices.

        Args:
        - stock_prices (list): The list of stock prices to analyze.

        Returns:
        - np.array: A numpy array indicating the length and direction of each streak. Positive values indicate a streak of 
        increasing prices, negative values indicate a streak of decreasing prices.
        """

        # Convert the list of stock prices to a DataFrame for easier manipulation.
        stock_df = pd.DataFrame(stock_prices)

        # Create two boolean Series that indicate where the current price is less than or equal to the previous price.
        # These Series are used to identify where streaks start and end.
        less_than_prev = stock_df[0] < stock_df[0].shift(1)
        equal_to_prev = stock_df[0] == stock_df[0].shift(1)

        # The row_count function calculates the length of each streak. 
        # If the streak is of decreasing prices, it returns a negative value.
        def row_count(current_group, cumulative_sum=[0, 0]):

            # Start counting from 0 unless the previous price was equal to the current one, 
            # in which case we start from 1 to avoid counting the same price twice.
            start_row = 0 if cumulative_sum[0] == 0 or equal_to_prev[cumulative_sum[1]] else 1

            # Generate a range of numbers representing the length of the streak.
            group_rows = np.arange(start_row, len(current_group) + start_row)

            # If we are on an odd-numbered streak, the prices are decreasing, so we negate the range to indicate this.
            if cumulative_sum[0] % 2 == 1:
                group_rows = -group_rows

            # Update the total number of streaks and total length of all streaks for use in the next call to row_count.
            cumulative_sum[0] += 1
            cumulative_sum[1] += len(current_group)

            # Return the range as a Series, with the index preserved from the original DataFrame.
            return pd.Series(group_rows, current_group.index)

        # Group the rows based on whether the price is increasing or decreasing. 
        # The cumsum function ensures that each group represents a single streak.
        streak_groups = (less_than_prev != less_than_prev.shift(1)).cumsum()

        # Apply the row_count function to each group to get the length and direction of each streak.
        return np.array(stock_df.groupby(streak_groups).apply(row_count), dtype=float)


    def percentile(self, time_series):
        """
        This function computes the percentile rank of the last value in a time series.

        Args:
        - time_series (pd.Series): The time series to analyze.

        Returns:
        - float: The percentile rank of the last value in the time series.
        """
        # The percentile rank is the proportion of values in the time series less than the last value.
        return time_series[time_series < time_series.iloc[-1]].count() / (time_series.count() - 1)


    def percent_rank(self, prices, lookback):
        """
        This function computes the percentile rank of each value in a price series over a rolling window.

        Args:
        - prices (pd.Series): The price series to analyze.
        - lookback (int): The number of previous values to consider when computing the percentile rank.

        Returns:
        - pd.Series: A series where each value is the percentile rank of the corresponding value in the input series.
        """
        # Compute the percentage change for each price
        pct_change = prices.pct_change()
        
        # Apply the percentile function over a rolling window
        pct_rank = pct_change.rolling(window=lookback + 1, center=False).apply(self.percentile, raw=False).fillna(0)

        # Multiply the percentile rank by 100 to convert to percentage terms
        return pct_rank * 100


    def calc_connors_rsi(self):
        """
        This function calculates the Connors RSI, which is an indicator that combines the regular RSI, 
        the RSI of a streak, and the percent rank of the price.

        Returns:
        - pd.Series: A series representing the Connors RSI.
        """
        # Get the closing prices
        close_series = self.stock_df['close']
        close_numpy_array = self.stock_df['close'].to_numpy()

        # Calculate the regular RSI
        rsi = ta.RSI(close_numpy_array, self.rsi_len)
        
        # Calculate the RSI of a streak
        streak_rsi = ta.RSI(self.streaks(close_numpy_array), self.streak_len)
        
        # Calculate the percent rank of the closing price
        rank = self.percent_rank(close_series, self.percent_rank_len)

        # The Connors RSI is the average of the three components
        return (rsi + streak_rsi + rank) / 3
