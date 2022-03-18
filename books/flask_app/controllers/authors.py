from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.author import Author #<--models.(fileName) import (className)
from flask_app.models.book import Book
@app.route('/')
@app.route('/authors')
def authors():
    authors = Author.get_all()
    return render_template('authors.html', authors = authors)

@app.route('/authors/<int:id>')
def showAuthor(id):
    data = {
        'id' : id
    }
    author = Author.get_author_with_favorites(data)
    books = Book.get_all_unfavorited(data)
    return render_template("authors_show.html", author = author, books = books)

@app.route('/create_author', methods=['POST'])
def createAuthor():
    data = {
        'name' : request.form['name']
    }
    Author.save(data)
    return redirect('/')

@app.route('/create_favorite', methods=['POST'])
def createFavorite():
    data = {
        'author_id' : request.form['author_id'],
        'book_id' : request.form['book_id']
        
    }
    Author.save_author_favorite_book(data)
    return redirect(f"/authors/{data['author_id']}")
