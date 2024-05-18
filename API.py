from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Mysql123!@localhost/mylibrary'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    published_date = db.Column(db.String(20), nullable=False)
    isbn_number = db.Column(db.String(20), nullable=False)

    def __init__(self, title, author, published_date, isbn_number):
        self.title = title
        self.author = author
        self.published_date = published_date
        self.isbn_number = isbn_number


class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author', 'published_date', 'isbn_number')

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    try:
        new_book = Book(
            title=data['title'],
            author=data['author'],
            published_date=data['published_date'],
            isbn_number=data['isbn_number']
        )
        db.session.add(new_book)
        db.session.commit()
        return book_schema.jsonify(new_book), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
