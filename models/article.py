import sqlite3
from database.connection import get_db_connection 
from models.author import Author  
from models.magazine import Magazine  

class Article:
    def __init__(self, title, content, author, magazine):
        self.title = title  # Set the article's title 
        self.content = content  # Set the article's content
        self.author = author  # Set the article's author (an Author object)
        self.magazine = magazine  # Set the article's magazine 
        self.id = self.create_article(title, content, author, magazine)  # Create a new article in the database and set the article ID

    def create_article(self, title, content, author, magazine):
        conn = get_db_connection()  
        cursor = conn.cursor() 
        cursor.execute('''
            INSERT INTO articles (title, content, author_id, magazine_id) 
            VALUES (?, ?, ?, ?)  # Insert the article details into the articles table
        ''', (title, content, author.id, magazine.id))  # Pass in the article details (including author ID and magazine ID)
        conn.commit() 
        article_id = cursor.lastrowid  # Get the ID of the newly inserted article
        conn.close() 
        return article_id  

    # Getter for the article's title property
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if 5 <= len(value) <= 50:  # Check if the title length is within 5 and 50 characters
            self._title = value  # Set the article's title
        else:
            raise ValueError("Article title must be between 5 and 50 characters.") 
    def author(self):
        conn = get_db_connection()  
        cursor = conn.cursor() 
        cursor.execute('SELECT * FROM authors WHERE id = ?', (self.author_id,))  # Query the authors table for the author by ID
        author = cursor.fetchone()  # Fetch the author data
        conn.close() 
        return Author(author[1]) if author else None  # Return an Author object if found, otherwise return None

    def magazine(self):
        conn = get_db_connection() 
        cursor = conn.cursor() 
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (self.magazine_id,))  # Query the magazines table for the magazine by ID
        magazine = cursor.fetchone()  # Fetch the magazine data
        conn.close() 
        return Magazine(magazine[1], magazine[2]) if magazine else None  # Return a Magazine object if found, otherwise return None
