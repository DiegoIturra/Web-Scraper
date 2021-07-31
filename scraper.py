import requests
from bs4 import BeautifulSoup

class Scraper:

	URL = "https://literaturalibertad.com/collections/all?page="
	
	#Get name for every book
	def __getBookName(self,soup):
		return [divtag.text for divtag in soup.find_all('div',{'class':'h4'})]

	#Get original price for every book
	def __getBookPrice(self,soup):
		prices = []
		for divtag in soup.find_all('div',{'class':'price__regular'}):
			for spanTag in divtag.find('span',{'class':'price-item price-item--regular'}):
				prices.append(spanTag)
		return prices


	#Get count of total pages for scraping
	def __getTotalPages(self,soup):
		textPages = soup.find('li',{'class':'pagination__text'}).text
		textList = textPages.strip().split(' ')
		return int(textList[len(textList)-1])

	#Get the link to the book data
	def __getBookPath(self,soup):
		return [path['href'] for path in soup.find_all('a',{'class':'grid-view-item__link grid-view-item__image-container full-width-link'})]


	#Get data from all pages
	def doScraping(self):
		request = requests.get(self.URL)
		soup = BeautifulSoup(request.text,'html.parser')

		numPages = self.__getTotalPages(soup)
		bookNames = []
		for page in range(1,numPages+1):
			url = self.URL + str(page)
			request = requests.get(url)
			soup = BeautifulSoup(request.text,'html.parser')
			currentBookNames = self.__getBookName(soup)

			for current in currentBookNames:
				bookNames.append(current)



		return "Success!"

