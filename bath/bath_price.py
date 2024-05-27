import datetime

import holidays

today = datetime.date.today()

ru_holidays = holidays.country_holidays('RU')

print(datetime.date(2024, 6, 12) in ru_holidays)


# def get_price(ordered_date, time_slot):
#     if (datetime.date.fromisoformat(ordered_date).isoweekday() < 6 and
#             time_slot):