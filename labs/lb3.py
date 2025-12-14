# Завдання 1
# [
#     {
#         "exchangedate": "07.12.2025",
#         "r030": 840,
#         "cc": "USD",
#         "txt": "Долар США",
#         "enname": "US Dollar",
#         "rate": 42.1838,
#         "units": 1,
#         "rate_per_unit": 42.1838,
#         "group": "1",
#         "calcdate": "04.12.2025"
#     },
#     {
#         "exchangedate": "08.12.2025",
#         "r030": 840,
#         "cc": "USD",
#         "txt": "Долар США",
#         "enname": "US Dollar",
#         "rate": 42.0567,
#         "units": 1,
#         "rate_per_unit": 42.0567,
#         "group": "1",
#         "calcdate": "05.12.2025"
#     },
#     {
#         "exchangedate": "09.12.2025",
#         "r030": 840,
#         "cc": "USD",
#         "txt": "Долар США",
#         "enname": "US Dollar",
#         "rate": 42.07,
#         "units": 1,
#         "rate_per_unit": 42.07,
#         "group": "1",
#         "calcdate": "08.12.2025"
#     },
#     {
#         "exchangedate": "10.12.2025",
#         "r030": 840,
#         "cc": "USD",
#         "txt": "Долар США",
#         "enname": "US Dollar",
#         "rate": 42.1838,
#         "units": 1,
#         "rate_per_unit": 42.1838,
#         "group": "1",
#         "calcdate": "09.12.2025"
#     },
#     {
#         "exchangedate": "11.12.2025",
#         "r030": 840,
#         "cc": "USD",
#         "txt": "Долар США",
#         "enname": "US Dollar",
#         "rate": 42.2812,
#         "units": 1,
#         "rate_per_unit": 42.2812,
#         "group": "1",
#         "calcdate": "10.12.2025"
#     },
#     {
#         "exchangedate": "12.12.2025",
#         "r030": 840,
#         "cc": "USD",
#         "txt": "Долар США",
#         "enname": "US Dollar",
#         "rate": 42.2721,
#         "units": 1,
#         "rate_per_unit": 42.2721,
#         "group": "1",
#         "calcdate": "11.12.2025"
#     },
#     {
#         "exchangedate": "13.12.2025",
#         "r030": 840,
#         "cc": "USD",
#         "txt": "Долар США",
#         "enname": "US Dollar",
#         "rate": 42.2721,
#         "units": 1,
#         "rate_per_unit": 42.2721,
#         "group": "1",
#         "calcdate": "11.12.2025"
#     },
#     {
#         "exchangedate": "14.12.2025",
#         "r030": 840,
#         "cc": "USD",
#         "txt": "Долар США",
#         "enname": "US Dollar",
#         "rate": 42.2721,
#         "units": 1,
#         "rate_per_unit": 42.2721,
#         "group": "1",
#         "calcdate": "11.12.2025"
#     }
# ]

import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=7)

#Завдання 2
url = "https://bank.gov.ua/NBU_Exchange/exchange_site"
params = {
    "start": start_date.strftime('%Y%m%d'),
    "end": end_date.strftime('%Y%m%d'),
    "valcode": "usd",
    "sort": "exchangedate",
    "order": "asc",
    "json": ""
}

response = requests.get(url, params=params)
data = response.json()

print(f"Отримано записів: {len(data)}")
for item in data:
    print(f"Дата: {item['exchangedate']} | Курс: {item['rate']}")

#Завдання 3
dates = [item['exchangedate'] for item in data]
rates = [item['rate'] for item in data]

plt.figure(figsize=(10, 6))
plt.plot(dates, rates, marker='o', label='USD')

plt.title(f'Курс USD з {dates[0]} по {dates[-1]}')
plt.xlabel('Дата')
plt.ylabel('Курс (UAH)')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()