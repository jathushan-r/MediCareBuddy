import datetime

day_index = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6
    }

def get_latest_date_for_day(target_day):
    # Get the current datetime
    print(target_day)
    current_datetime = datetime.datetime.now()
    print(current_datetime)
    # Get the current day of the week (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
    current_day = current_datetime.weekday()
    print(current_day)

    # Get the target day of the week
    target_day_index = day_index.get(target_day.lower())
    print(target_day_index)

    # Calculate the number of days to add to the current date to reach the target day
    days_to_add = (target_day_index - current_day + 7) % 7 

    if days_to_add == 0:
        days_to_add = 7

    # Calculate the latest date for the target day
    latest_date = current_datetime + datetime.timedelta(days=days_to_add)

    return latest_date

# Example usage:
# target_day = 'MoNdAy'
# latest_date = get_latest_date_for_day(target_day)
# print(latest_date.date())