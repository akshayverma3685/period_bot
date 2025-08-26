from datetime import datetime, timedelta

def calculate_next_period(last_period_str, cycle_length=28):
    last_period = datetime.strptime(last_period_str, "%d-%m-%Y")
    next_period = last_period + timedelta(days=cycle_length)
    return next_period.strftime("%d-%m-%Y")

def calculate_fertile_window(last_period_str, cycle_length=28):
    last_period = datetime.strptime(last_period_str, "%d-%m-%Y")
    ovulation_day = last_period + timedelta(days=cycle_length - 14)
    fertile_start = ovulation_day - timedelta(days=2)
    fertile_end = ovulation_day + timedelta(days=2)
    return fertile_start.strftime("%d-%m-%Y"), fertile_end.strftime("%d-%m-%Y")
