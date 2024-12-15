import sqlite3
from database.connection import get_db_connection

class Magazine:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.id = self.create_magazine(name, category)

    def create_magazine(self, name, category):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (name, category))
        conn.commit()
        magazine_id = cursor.lastrowid
        conn.close()
        return magazine_id

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Magazine name must be between 2 and 16 characters.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if len(value) > 0:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string.")

    @id.setter
    def id(self, value):
        self._id = value  # Now we are setting the _id attribute using the setter        

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article[0], article[1], article[2], article[3], article[4]) for article in articles]

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT authors.* FROM authors '
                       'JOIN articles ON articles.author_id = authors.id '
                       'WHERE articles.magazine_id = ?', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author[1]) for author in authors]

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self.id,))
        titles = cursor.fetchall()
        conn.close()
        return [title[0] for title in titles] if titles else None

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.name FROM authors
            JOIN articles ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2
        ''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return [author[0] for author in authors] if authors else None
