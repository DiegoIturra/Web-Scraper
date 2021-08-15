from extensions import db,marshmallow


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    title_for_route = db.Column(db.String(40), nullable=False)
    price = db.Column(db.String(40), nullable=False)
    url = db.Column(db.String(40), nullable=False)

    
    def __repr__(self):
        return f"{self.id} => {self.title} => {self.price} => {self.url}"

class BookSchema(marshmallow.SQLAlchemySchema):
    
    class Meta:
        model = Book

    id = marshmallow.auto_field()
    title = marshmallow.auto_field()
    title_for_route = marshmallow.auto_field()
    price = marshmallow.auto_field()
    url = marshmallow.auto_field()

