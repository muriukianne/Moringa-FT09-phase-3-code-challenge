import sqlite3
from database.connection import get_db_connection  

class Magazine:
    def __init__(self, name, category):
        self.name = name  
        self.category = category 
        self.id = self.create_magazine(name, category)  # Create a new magazine record in the database and store the ID

    def create_magazine(self, name, category):
        conn = get_db_connection() 
        cursor = conn.cursor() 
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (name, category))  # Insert magazine details into the table
        conn.commit()  
        magazine_id = cursor.lastrowid  # Get the ID of the newly inserted magazine
        conn.close() 
        return magazine_id  

    # Getter for the magazine's ID property
    @property
    def id(self):
        return self._id

    # Getter for the magazine's name property
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if 2 <= len(value) <= 16:  # Check if the name length is between 2 and 16 characters
            self._name = value 
        else:
            raise ValueError("Magazine name must be between 2 and 16 characters.")

    # Getter for the magazine's category property
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if len(value) > 0:  # Ensure category is a non-empty string
            self._category = value  
        else:
            raise ValueError("Category must be a non-empty string.")  

    # Setter for the magazine's ID property
    @id.setter
    def id(self, value):
        self._id = value  # Set the magazine's ID using the setter

    def articles(self):
        conn = get_db_connection() 
        cursor = conn.cursor()  
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self.id,))  # Select articles based on magazine ID
        articles = cursor.fetchall()  # Fetch all articles associated with the magazine
        conn.close() 
        # Return a list of Article objects created using the fetched article data
        return [Article(article[0], article[1], article[2], article[3], article[4]) for article in articles]

    def contributors(self):
        conn = get_db_connection()  
        cursor = conn.cursor() 
        cursor.execute('SELECT DISTINCT authors.* FROM authors '
                       'JOIN articles ON articles.author_id = authors.id '
                       'WHERE articles.magazine_id = ?', (self.id,))  # Select authors who have contributed to this magazine
        authors = cursor.fetchall()  # Fetch all authors associated with the magazine
        conn.close()  
        # Return a list of Author objects created using the fetched author data
        return [Author(author[1]) for author in authors]

    def article_titles(self):
        conn = get_db_connection()  
        cursor = conn.cursor()  
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self.id,))  # Select article titles based on magazine ID
        titles = cursor.fetchall()  # Fetch all article titles
        conn.close() 
        return [title[0] for title in titles] if titles else None  # Return a list of titles if found, otherwise None

    def contributing_authors(self):
        conn = get_db_connection() 
        cursor = conn.cursor() 
        cursor.execute('''
            SELECT authors.name FROM authors
            JOIN articles ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2  # Select authors who have contributed more than two articles
        ''', (self.id,))  # Pass the magazine ID as a parameter to the query
        authors = cursor.fetchall()  # Fetch the contributing authors
        conn.close() 
        return [author[0] for author in authors] if authors else None  # Return a list of author names if found, otherwise None
