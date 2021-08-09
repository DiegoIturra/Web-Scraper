from extensions import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    price = db.Column(db.String(40), nullable=False)
    url = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f"{self.id} => {self.title} => {self.price} => {self.url}"
