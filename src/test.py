from datetime import date

today = date.today()
week_day = today.weekday()
print(week_day)
today = today.replace(day=today.day - week_day)
print(today.isoformat())
