from database.setup import create_tables
from database.connection import get_db_connection

def main():
    # Initialize the database and create tables
    create_tables()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Create an author
    cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
    author_id = cursor.lastrowid  # Use this to fetch the id of the newly created author

    # Create a magazine
    cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (magazine_name, magazine_category))
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
        print(f'Magazine {magazine["id"]}, Name: {magazine["name"]}, Category: {magazine["category"]}')

    print("\nAuthors:")
    for author in authors:
       print(f'Author {author["id"]}, Name: {author["name"]}')

    print("\nArticles:")
    for article in articles:
         print(f'Article {article["id"]}, Title: {article["title"]}, Content: {article["content"]}, '
              f'Author ID: {article["author_id"]}, Magazine ID: {article["magazine_id"]}')
"""  """
if __name__ == "__main__":
    main()
