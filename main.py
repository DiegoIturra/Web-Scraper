from flask import Flask,jsonify
from scraper import Scraper
from flask_apscheduler import APScheduler


if __name__ == "__main__":

	scraper = Scraper()
	data = scraper.scrapingData()

	for dictionary in data:
		print(f"{dictionary['title']} => {dictionary['price']} => {dictionary['link']}")

