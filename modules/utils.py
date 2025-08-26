# modules/utils.py
from datetime import datetime, timedelta

def calculate_next_period(last_period_str, cycle_length):
    last_period = datetime.strptime(last_period_str, '%d-%m-%Y')
    next_period = last_period + timedelta(days=cycle_length)
    return next_period.strftime('%d-%m-%Y')

def get_today_date():
    return datetime.now().strftime('%Y-%m-%d')
