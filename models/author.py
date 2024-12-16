import sqlite3
from database.connection import get_db_connection  

class Author:
    def __init__(self, name):
        self.name = name  # Set the author's name 
        self.id = self.create_author(name)  # Created a new author record in the database and store the ID

    def create_author(self, name):
        conn = get_db_connection()  # Get a database connection
        cursor = conn.cursor()  
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (name,))  # Insert the author's name into the authors table
        conn.commit()  
        author_id = cursor.lastrowid  # Get the ID of the newly inserted author
        conn.close() 
        return author_id  # Return the new author's ID

    # Getter for the author's ID property
    @property
    def id(self):
        return self._id

    # Getter for the author's name property
    @property
    def name(self):
        return self._name

    # Setter for the author's name property, ensures name is non-empty
    @name.setter
    def name(self, value):
        if len(value) > 0:  # Check if the name is a non-empty string
            self._name = value  
        else:
            raise ValueError("Author name must be a non-empty string")  # Raise an error if name is empty

    # Setter for the author's ID property
    @id.setter
    def id(self, value):
        self._id = value  # Set the author's ID

    def articles(self):
        conn = get_db_connection()  
        cursor = conn.cursor()  
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))  # Select articles based on author ID
        articles = cursor.fetchall()  # Fetch all articles associated with the author
        conn.close() 
        # Return a list of Article objects created using the fetched article data
        return [Article(article[0], article[1], article[2], article[3], article[4]) for article in articles]

    def magazines(self):
        conn = get_db_connection() 
        cursor = conn.cursor()  
        cursor.execute('SELECT DISTINCT magazines.* FROM magazines '
                       'JOIN articles ON articles.magazine_id = magazines.id '
                       'WHERE articles.author_id = ?', (self.id,))  # Select magazines associated with the author
        magazines = cursor.fetchall()  # Fetch all distinct magazines associated with the author
        conn.close() 
        # Return a list of Magazine objects created using the fetched magazine data
        return [Magazine(magazine[0], magazine[1], magazine[2]) for magazine in magazines]
