from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    '''
        The following is just for testing purposes,
        you can modify it to meet the requirements of your implementation.
    '''

    # Create an author
    cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
    author_id = cursor.lastrowid  # Use this to fetch the id of the newly created author

    # Create a magazine
    cursor.execute('INSERT INTO magazines (name, category) VALUES (?,?)', (magazine_name, magazine_category))
    magazine_id = cursor.lastrowid  # Use this to fetch the id of the newly created magazine

    # Create an article
    cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                   (article_title, article_content, author_id, magazine_id))

    conn.commit()

    # Query the database for inserted records.
    # The following fetch functionality should probably be in their respective models
    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    conn.close()

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        # Create Magazine object with name and category only
        magazine_obj = Magazine(magazine[1], magazine[2])  # Magazine(name, category)
        magazine_obj.id = magazine[0]  # Manually set the ID
        print(f"ID: {magazine_obj.id}, Name: {magazine_obj.name}, Category: {magazine_obj.category}")

    print("\nAuthors:")
    for author in authors:
        # Create Author object with name only
        author_obj = Author(author[1])  # Author(name)
        author_obj.id = author[0]  # Manually set the ID
        print(f"ID: {author_obj.id}, Name: {author_obj.name}")

    print("\nArticles:")
    for article in articles:
        # Create Article object, use Author and Magazine to link them
        author_obj = Author(article[3])  # Fetch the author (ID 3 in the query result)
        magazine_obj = Magazine(article[4])  # Fetch the magazine (ID 4 in the query result)
        article_obj = Article(article[1], article[2], author_obj, magazine_obj)  # Article(title, content, author, magazine)
        article_obj.id = article[0]  # Manually set the ID
        print(f"ID: {article_obj.id}, Title: {article_obj.title}, Author: {article_obj.author().name}, Magazine: {article_obj.magazine().name}")

if __name__ == "__main__":
    main()
