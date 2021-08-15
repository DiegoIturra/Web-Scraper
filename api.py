from flask import Blueprint,jsonify
from models import Book,BookSchema

main = Blueprint('main', __name__)

    
@main.route("/books", methods=['GET'])
def get_books():
    books = Book.query.all()
    book_schema = BookSchema(many=True)
    output = book_schema.dump(books)
    return jsonify(output)


@main.route("/book/<int:id>", methods=['GET'])
def get_books_by_id(id):
    book = Book.query.get(id)
    book_schema = BookSchema()
    output = book_schema.dump(book)
    return jsonify(output)


@main.route("/book/<title>", methods=['GET'])
def get_books_by_title(title):
    """ Title should be parsed without spaces """
    book = Book.query.filter_by(title_for_route=title).first()
    book_schema = BookSchema()
    output = book_schema.dump(book)
    return jsonify(output)
