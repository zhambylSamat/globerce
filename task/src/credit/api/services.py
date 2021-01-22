from .constants import HOLIDAY_API_URL
import requests
from datetime import datetime


def get_holidays():
	response = requests.get(HOLIDAY_API_URL)
	return [{'name': item['name'], 'date': item['date']} for item in response.json()['holidays']]


def get_holiday_by_date(date):
	for item in get_holidays():
		if datetime.strptime(item['date'], '%Y-%m-%d').date() == date:
			return item
	return None
