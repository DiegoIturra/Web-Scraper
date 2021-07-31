import requests
from bs4 import BeautifulSoup

class Scraper:

	URL = "https://literaturalibertad.com/collections/all?page="
	
	#Get name for every book
	def __getBookName(self,soup):
		names = soup.find_all('div',{'class':'h4'})
		bookNames = []
		for bookName in names:
			bookName = Utils.translateText(bookName.text.strip())
			bookNames.append(bookName)
		return bookNames

		
	#Get original price for every book
	def __getBookPrices(self,soup):
		prices = []
		for divtag in soup.find_all('div',{'class':'price__regular'}):
			for spanTag in divtag.find('span',{'class':'price-item price-item--regular'}):
				prices.append(spanTag.strip())
		return prices


	#Get count of total pages for scraping
	def __getTotalPages(self,soup):
		textPages = soup.find('li',{'class':'pagination__text'}).text
		textList = textPages.strip().split(' ')
		return int(textList[len(textList)-1])

	#Get the link to the book data
	def __getBookPath(self,soup):
		return [path['href'] for path in soup.find_all('a',{'class':'grid-view-item__link grid-view-item__image-container full-width-link'})]
		

	#Get the image path from each book
	def __getImagePath(self,soup):
		pass


	#Get data from all pages
	def doScraping(self):
		request = requests.get(self.URL)
		soup = BeautifulSoup(request.text,'html.parser')

		numPages = self.__getTotalPages(soup)
		bookNames = []
		bookPrices = []
		for page in range(1,numPages+1):
			url = self.URL + str(page)
			request = requests.get(url)
			soup = BeautifulSoup(request.text,'html.parser')
			
			currentBookNames = self.__getBookName(soup)
			currentBookPrices = self.__getBookPrices(soup)

			for currentName in currentBookNames:
				bookNames.append(currentName)
			
			for currentPrice in currentBookPrices:
				bookPrices.append(currentPrice)
		
		dictionary = dict(zip(bookNames,bookPrices))
		return dictionary


class Utils:

	@staticmethod
	def translateText(text):
		""" method to translate latin characters """
		charsToTranslate = "ÁÉÍÓÚáéíóoúñ"
		objectiveText = "AEIOUaeioun"
		try:
			translation = str.maketrans(charsToTranslate,objectiveText)
			return text.translate(translation)
		except:
			return text
		

