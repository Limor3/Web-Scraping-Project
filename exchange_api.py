import configuration as cfg
import requests
from datetime import date
"""
This file get price exchange rate by API.
"""

today = date.today()

response = requests.get(cfg.API_REQUEST.format(today, cfg.BASE_EX_RATE, cfg.SYMBOL_EX_RATE))
data = response.json()
exchange_rate = data[cfg.GET_RATE_JASON_EX][cfg.SYMBOL_EX_RATE]
date_exchange_rate = data[cfg.GET_DATE_JASON_EX]
