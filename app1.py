from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # Changed database name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'
@app.route('/', methods=['GET'])
def landing_page():
    return render_template('landing.html')  # Display landing page

@app.route('/books/', methods=['POST', 'GET'])
def books():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        publication_date = datetime.strptime(request.form['publication_date'], '%Y-%m-%d')  # Date format
        price = float(request.form['price'])

        new_book = Book(title=title, author=author, genre=genre, publication_date=publication_date, price=price)

        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect('/books/')
        except:
            return 'There was an issue adding your book'

    else:
        books = Book.query.order_by(Book.publication_date).all()  # Show all books
        return render_template('books.html', books=books)  # Render book list page


@app.route('/delete/<int:id>')
def delete(id):
    book_to_delete = Book.query.get_or_404(id)

    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect('/books/')
    except:
        return 'There was a problem deleting that book'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    book = Book.query.get_or_404(id)

    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.publication_date = datetime.strptime(request.form['publication_date'], '%Y-%m-%d')
        book.price = float(request.form['price'])

        try:
            db.session.commit()
            return redirect('/books/')
        except:
            return 'There was an issue updating your book'

    return render_template('update_book.html', book=book)  # Render update page for the book
if __name__ == "__main__":
    app.run(debug=True)

