from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.book import Book #<--models.(fileName) import (className)
from flask_app.models.author import Author
#place all @app.routes here change file name to plural of class

@app.route('/books')
def books():
    books = Book.get_all()
    return render_template('books.html', books = books)

@app.route('/books/<int:id>')
def showBook(id):
    data = {
        'id' : id
    }
    book = Book.get_book_with_favorites(data)
    authors = Author.get_all_unfavorited(data)
    return render_template('books_show.html', book = book, authors = authors)

@app.route('/create_book', methods=['POST'])
def createBook():
    data = {
        'title' : request.form['title'],
        'num_of_pages' : request.form['num_of_pages']
    }
    Book.save(data)
    return redirect('/books',)

@app.route('/add_favorite', methods=['POST'])
def addFavorite():
    data = {
        'book_id' : request.form['book_id'],
        'author_id' : request.form['author_id']
        
    }
    Book.save_book_favorite_author(data)
    return redirect(f"/books/{data['book_id']}")