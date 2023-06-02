from datetime import datetime
from main_trade_stocks import run_stock_script
from main_trade_options import run_option_script

def check_file_for_catalyst():
    """
    Check if today is a market catalyst date by comparing it with
    a list of dates from a text file.

    Returns:
        bool: True if today is a market catalyst date, False otherwise.
    """
    # Open the file and read the dates
    with open('market_dates.txt', 'r') as f:
        dates = f.read().splitlines()

    # Convert strings to datetime objects
    dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates]

    # Check if today is in the list
    today = datetime.today().date()

    if today in dates:
        print(f"\nToday ({today}) is a market catalyst date.\n")
        return True
    else:
        print(f"\nToday ({today}) is not a market catalyst date.\n")
        return False

def main():
    """
    Main function that checks if today is a market catalyst date and prompts
    the user to choose which script to run based on their input.

    Returns:
        None
    """
    catalyst_today = check_file_for_catalyst()

    if not catalyst_today:
        choice = input("Enter 1 for the first script (stocks) or 2 for the second script (options): ")
        
        if choice == "1":
            print("Running stocks script...")
            run_stock_script()
        elif choice == "2":
            print("Running options script...")
            run_option_script()
        else:
            print("Invalid input. Please enter 1 or 2.")

if __name__ == "__main__":
    main()