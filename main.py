from flask import Flask
from scraper import Scraper

app = Flask(__name__)

@app.route('/')
def index():
	scraperObject = Scraper()
	return scraperObject.doScraping()

if __name__ == '__main__':
	app.run(debug=True)