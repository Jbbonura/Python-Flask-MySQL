from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author
class Book:
    def __init__(self, data):
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []

    @classmethod
    def get_all(cls):
        query="SELECT * FROM books;"
        results=connectToMySQL('books_schema').query_db(query)

        books = []

        for book in results:
            books.append(cls(book))
        return books

    @classmethod
    def get_one(cls, data):
        query="SELECT * FROM books WHERE id = %(id)s;"
        book = connectToMySQL('books_schema').query_db(query, data)
        return cls(book[0])

    @classmethod
    def get_one_by_name(cls, data):
        query="SELECT * FROM books WHERE title = %(title)s;"
        book = connectToMySQL('books_schema').query_db(query, data)
        print(book[0])
        return cls(book[0])

    @classmethod
    def save(cls, data):
        query="INSERT INTO books (title, num_of_pages, created_at, updated_at) VALUES (%(title)s, %(num_of_pages)s, NOW(), NOW());"
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def get_book_with_favorites(cls, data):
        query="SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN authors ON favorites.author_id = authors.id WHERE books.id = %(id)s;"
        results = connectToMySQL('books_schema').query_db(query, data)

        book = cls(results[0])

        for row_from_db in results:
            author_data = {
                'id' : row_from_db['authors.id'],
                'name' : row_from_db['name'],
                'created_at' : row_from_db['authors.created_at'],
                'updated_at' : row_from_db['authors.updated_at']
            }
            book.authors.append(author.Author(author_data))
        return book
    
    @classmethod
    def save_book_favorite_author(cls, data):
        query ="INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def get_all_unfavorited(cls, data):
        query= "SELECT * FROM books WHERE books.id NOT IN (SELECT book_id FROM favorites WHERE author_id = %(id)s);"
        results = connectToMySQL('books_schema').query_db(query, data)
        
        books = []
        for row in results:
            books.append(cls(row))
        return books