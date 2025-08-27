from datetime import datetime, timedelta

def calculate_next_period(last_period_date: str, cycle_length: int) -> str:
    """
    Calculate the expected next period date.

    Parameters:
    - last_period_date (str): Last period date in DD-MM-YYYY format
    - cycle_length (int): Length of menstrual cycle in days

    Returns:
    - str: Next period date in DD-MM-YYYY format
    """
    try:
        last_period = datetime.strptime(last_period_date, "%d-%m-%Y")
        next_period = last_period + timedelta(days=cycle_length)
        return next_period.strftime("%d-%m-%Y")
    except ValueError:
        return "Invalid date format. Please use DD-MM-YYYY."
