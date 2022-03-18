from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    def __init__(self, data):
        self.name = data['name']
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []

    @classmethod
    def get_all(cls):
        query="SELECT * FROM authors;"
        results=connectToMySQL('books_schema').query_db(query)

        authors = []

        for author in results:
            authors.append(cls(author))
        return authors

    @classmethod
    def get_one(cls, data):
        query="SELECT * FROM authors WHERE id = %(id)s;"
        author = connectToMySQL('books_schema').query_db(query, data)
        return cls(author[0])
    
    @classmethod
    def get_one_by_name(cls, data):
        query="SELECT * FROM authors WHERE name = %(name)s;"
        author = connectToMySQL('books_schema').query_db(query, data)
        return cls(author[0])

    @classmethod
    def save(cls, data):
        query="INSERT INTO authors (name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW());"
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def get_author_with_favorites(cls, data):
        query="SELECT * FROM authors LEFT JOIN favorites ON favorites.author_id = authors.id LEFT JOIN books ON favorites.book_id = books.id WHERE authors.id = %(id)s;"
        results = connectToMySQL('books_schema').query_db(query, data)
        
        author = cls (results[0])
        print(author.id)
        for row_from_db in results:
            book_data = {
                'id' : row_from_db['books.id'],
                'title' : row_from_db['title'],
                'num_of_pages' : row_from_db['num_of_pages'],
                'created_at' : row_from_db['books.created_at'],
                'updated_at' : row_from_db['books.updated_at']
            }
            author.books.append(book.Book(book_data))
        return author
    
    @classmethod
    def save_author_favorite_book(cls, data):
        query ="INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def get_all_unfavorited(cls, data):
        query= "SELECT * FROM authors WHERE authors.id NOT IN (SELECT author_id FROM favorites WHERE book_id = %(id)s);"
        results = connectToMySQL('books_schema').query_db(query, data)
        
        authors = []
        for row in results:
            authors.append(cls(row))
        return authors
