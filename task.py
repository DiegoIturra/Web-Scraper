from scraper import Scraper
from extensions import scheduler,db
from models import Book


class BooksObject:
    """ A cache of objects """

    def __init__(self):
        self.list_of_books = []

    def get_list_of_books(self):
        return self.list_of_books

    def set_list_of_books(self,list_of_books):
        self.list_of_books = list_of_books


scraper = Scraper()
bookObject = BooksObject()


@scheduler.task("cron", id="job_1", hour=19, minute=14)
def get_data_from_web_page():
    print("Starting scraper..")
    scraping_data = scraper.scrapingData()
    list_of_books = []
    with scheduler.app.app_context():
        for data in scraping_data:
            title_list = data["title"].split(' ')
            title_for_route = "".join(title_list)
            list_of_books.append(Book(title=data['title'],title_for_route=title_for_route,price=data['price'],url=data['link']))
    bookObject.set_list_of_books(list_of_books)
    print("Scraper has finished succesfully!")


@scheduler.task("cron" , id="job_2", hour=19, minute=15)
def update_data_from_web_page():
    print("Updating data..")
    list_of_books = bookObject.get_list_of_books()

    with scheduler.app.app_context():
        for book in list_of_books:
            #query if the book exists in database
            current_book = Book.query.filter_by(title=book.title).first()

            #if book does not exist in database , then add it to the database
            if current_book is None:
                db.session.add(book)
                db.session.commit()
            else:
                #update the current book
                current_book.price = book.price
                db.session.commit()
    print("Data updated succesfully!")