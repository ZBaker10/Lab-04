from flask import Flask
app = Flask(__name__)
from flask_sqllibrary import SQLLibrary

app.config['SQLLIBRARY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLLibrary(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(50), unique=True, nullable=False)
    author = db.Column(db.String(40), nullable=False)
    publisher = db.Column(db.String(60))

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"
    
@app.route('/')
def index():
    return 'Welcome to the library catalog.'

@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {'name': book.name, 'author': book.author, 'publisher': book.publisher}

        output.append(book_data)
    return {"books": output}
@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"name": book.name, "author": book.author, "publisher": book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(name=request.json['name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

@app.route('/books/<id>', method=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "deleted"}