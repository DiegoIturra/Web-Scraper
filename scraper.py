import requests
from bs4 import BeautifulSoup
import time

class Scraper:

	URL = "https://literaturalibertad.com/collections/all?page="
	mainURL = "https://literaturalibertad.com"
	
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
	def __getBookLink(self,soup):
		return [path['href'] for path in soup.find_all('a',{'class':'grid-view-item__link grid-view-item__image-container full-width-link'})]
		
	
	#Get data from all pages
	def scrapingData(self):
		request = requests.get(self.URL)
		soup = BeautifulSoup(request.text,'html.parser')

		numPages = self.__getTotalPages(soup)
		bookTitles = []
		bookPrices = []
		bookLinks = []
		for page in range(1,numPages+1):
			url = self.URL + str(page)
			request = requests.get(url)
			soup = BeautifulSoup(request.text,'html.parser')
			
			currentBookNames = self.__getBookName(soup)
			currentBookPrices = self.__getBookPrices(soup)
			currentBookLinks = self.__getBookLink(soup)

			#get title of books
			for currentName in currentBookNames:
				bookTitles.append(currentName)
			
			#get prices of books
			for currentPrice in currentBookPrices:
				bookPrices.append(currentPrice)

			#get links of books
			for currentLink in currentBookLinks:
				bookLinks.append(self.mainURL + currentLink)

		#list of dictionaries
		data = [{'title':title, 'price': price, 'link': link} for title, price, link in zip(bookTitles, bookPrices, bookLinks)]
		
		return data




class Utils:

	@staticmethod
	def translateText(text):
		""" method to translate latin characters """
		charsToTranslate = "ÁÉÍÓÚáéíóúñ"
		objectiveText = "AEIOUaeioun"
		try:
			translation = str.maketrans(charsToTranslate,objectiveText)
			return text.translate(translation)
		except:
			return text
		


