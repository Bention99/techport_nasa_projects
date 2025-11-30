import time
import re
from datetime import datetime


DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def user_input_information():
    time.sleep(1)
    print("To set the updated since parameter, please enter a date in the ISO 8601 format: YYYY-MM_DD:")
    valid_date = input_date()
    return valid_date

def input_date():
    date = input("> ")
    valid = check_date_validity(date)
    if valid:
        print("Valid")
        return date
    else:
        print("Input not valid. Format needs to be ISO 8601: YYYY-MM-DD. Please try again:")
        return input_date()

def check_date_validity(date):
    if not DATE_REGEX.match(date):
        return False

    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def projects_amount(total):
    print(f"Each download requires an API call. How many Projects do you want to download? The total amount is: {total}")
    amount = input("> ")
    amount = int(amount)
    if amount > total:
        print(f"The amount can't be more then the maximal amount of {total}")
        return None
    return amount