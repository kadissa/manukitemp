import datetime

import holidays

today = datetime.date.today()

ru_holidays = holidays.country_holidays('RU')

print(datetime.date(2024, 6, 12) in ru_holidays)


def get_price(ordered_date, time_slots: list) -> int:
    price = 0
    if time_slots:
        for time in time_slots:
            if datetime.date.fromisoformat(ordered_date).isoweekday() > 5:
                value = 2500
            elif (datetime.date.fromisoformat(ordered_date).isoweekday() == 5
                  and int(time[:2]) > 17):
                value = 2500
            else:
                value = 2000
            print(f'price: {price}, value: {value}, time_slots: '
                  f'{time_slots}, time: {time}')
            price += value
        return price
    else:
        return 0

