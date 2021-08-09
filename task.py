from scraper import Scraper
from extensions import scheduler,db
from models import Book

scraper = Scraper()

@scheduler.task("interval", id="job_1", seconds=180)
def get_data_from_web_page():
    print("Task from background in application factory")
    scraping_data = scraper.scrapingData()

    with scheduler.app.app_context():
        for data in scraping_data:
           db.session.add(Book(title=data['title'],price=data['price'],url=data['link']))
           db.session.commit()

        books = Book.query.all()
        for book in books:
            print(book)

        db.session.query(Book).delete()
        db.session.commit()