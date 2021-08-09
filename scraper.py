import requests
from bs4 import BeautifulSoup


class Scraper:
    URL = "https://literaturalibertad.com/collections/all?page="
    mainURL = "https://literaturalibertad.com"

    # Get name for every book
    def __get_book_names(self, soup: BeautifulSoup) -> list[str]:
        names = soup.find_all('div', {'class': 'h4'})
        bookNames = []
        for bookName in names:
            bookName = Utils.translate_text(bookName.text.strip())
            bookNames.append(bookName)
        return bookNames

    # Get original price for every book
    def __getBookPrices(self, soup: BeautifulSoup) -> list[str]:
        prices = []
        for divtag in soup.find_all('div', {'class': 'price__regular'}):
            for spanTag in divtag.find('span', {'class': 'price-item price-item--regular'}):
                prices.append(spanTag.strip())
        return prices

    # Get count of total pages for scraping
    def __getTotalPages(self, soup: BeautifulSoup) -> int:
        textPages = soup.find('li', {'class': 'pagination__text'}).text
        textList = textPages.strip().split(' ')
        return int(textList[len(textList) - 1])

    # Get the link to the book data
    def __getBookLink(self, soup: BeautifulSoup) -> list[str]:
        return [path['href'] for path in
                soup.find_all('a', {'class': 'grid-view-item__link grid-view-item__image-container full-width-link'})]

    # Get data from all pages
    def scrapingData(self) -> list[dict]:
        request = requests.get(self.URL)
        soup = BeautifulSoup(request.text, 'html.parser')

        num_pages = self.__getTotalPages(soup)
        book_titles = []
        book_prices = []
        book_links = []
        for page in range(1, num_pages + 1):
            url = self.URL + str(page)
            request = requests.get(url)
            soup = BeautifulSoup(request.text, 'html.parser')

            currentBookNames = self.__get_book_names(soup)
            currentBookPrices = self.__getBookPrices(soup)
            currentBookLinks = self.__getBookLink(soup)

            # get title of books
            for currentName in currentBookNames:
                book_titles.append(currentName)

            # get prices of books
            for currentPrice in currentBookPrices:
                book_prices.append(currentPrice)

            # get links of books
            for currentLink in currentBookLinks:
                book_links.append(self.mainURL + currentLink)

        # list of dictionaries
        data = [{'title': title, 'price': price, 'link': link} for title, price, link in
                zip(book_titles, book_prices, book_links)]

        return data


class Utils:

    @staticmethod
    def translate_text(text) -> str:
        """ method to translate latin characters """
        chars_to_translate = "ÁÉÍÓÚáéíóúñ"
        objective_text = "AEIOUaeioun"
        try:
            translation = str.maketrans(chars_to_translate, objective_text)
            return text.translate(translation)
        except:
            return text
