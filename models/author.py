import sqlite3
from database.connection import get_db_connection

class Author:
    def __init__(self, name):
        self.name = name
        self.id = self.create_author(name)

    def create_author(self, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (name,))
        conn.commit()
        author_id = cursor.lastrowid
        conn.close()
        return author_id

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if len(value) > 0:
            self._name = value
        else:
            raise ValueError("Author name must be a non-empty string")

    @id.setter
    def id(self, value):
        self._id = value

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article[0], article[1], article[2], article[3], article[4]) for article in articles]

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT magazines.* FROM magazines '
                       'JOIN articles ON articles.magazine_id = magazines.id '
                       'WHERE articles.author_id = ?', (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return [Magazine(magazine[0], magazine[1], magazine[2]) for magazine in magazines]
