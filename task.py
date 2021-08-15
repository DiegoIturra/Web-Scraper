from scraper import Scraper
from extensions import scheduler,db
from models import Book

scraper = Scraper()

@scheduler.task("interval", id="job_1", seconds=70)
def get_data_from_web_page():
    scraping_data = scraper.scrapingData()
    with scheduler.app.app_context():
        for data in scraping_data:
            title_list = data["title"].split(' ')
            title_for_route = "".join(title_list)
            db.session.add(Book(title=data['title'],title_for_route=title_for_route,price=data['price'],url=data['link']))
            db.session.commit()

        #db.session.query(Book).delete()
        #db.session.commit()