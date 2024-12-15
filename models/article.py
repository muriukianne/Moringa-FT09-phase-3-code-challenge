import sqlite3
from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, title, content, author, magazine):
        self.title = title
        self.content = content
        self.author = author
        self.magazine = magazine
        self.id = self.create_article(title, content, author, magazine)

    def create_article(self, title, content, author, magazine):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO articles (title, content, author_id, magazine_id) 
            VALUES (?, ?, ?, ?)
        ''', (title, content, author.id, magazine.id))
        conn.commit()
        article_id = cursor.lastrowid
        conn.close()
        return article_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if 5 <= len(value) <= 50:
            self._title = value
        else:
            raise ValueError("Article title must be between 5 and 50 characters.")

    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (self.author_id,))
        author = cursor.fetchone()
        conn.close()
        return Author(author[1]) if author else None

    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (self.magazine_id,))
        magazine = cursor.fetchone()
        conn.close()
        return Magazine(magazine[1], magazine[2]) if magazine else None
