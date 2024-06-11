


class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def find_by_id(cls, id):
        sql = """ 
            SELECT * FROM authors
            WHERE id = ?  
            SELECT * FROM magazines
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.find_by_id(row) if row else None

    def save(self):
        sql = """
        INSERT INTO articles
        (title, content, author_id, magazine_id)
        VALUES (?, ?, ?, ?)"""

        CURSOR.execute(sql, (self.title, self.content, self.author_id, self.magazine_id))
        CONN.commit()

        self.id = CURSOR.lastrowid

    def create(cls, id, title, content, author_id, magazine_id):
        article = cls(id, title, content, author_id, magazine_id)
        article.save()

    @classmethod
    def find_by_title(cls, title):
        sql = """ 
            SELECT * FROM articles
            WHERE title = ?
        """

        row = CURSOR.execute(sql, (title))
        return cls.instance_from_db(row) if row else None

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        if hasattr(self, '_title'):
            raise AttributeError("Title cannot be changed after the article is instantiated")
        if isinstance(title, str)and 5 <= len(title) >= 50:
            self._title = title
        else:
            raise TypeError("title must be of type string")
    @property
    def author(self):
        return self.find_by_id(self.author.id)
    
    @property
    def magazine(self):
        return self.find_by_id(self.magazine_id)
    
   #adding column author and magazine as a foreign key to articles table 
    sql = """ 
    ALTER TABLE articles ADD COLUMN author_id INTEGER;
    ALTER TABLE articles ADD COLUMN magazine_id INTEGER; 
 """

    @classmethod
    def get_author(cls, author_id):
        sql = """ 
            SELECT * FROM authors
            INNER JOIN articles
            ON authors.id = articles.author_id;
        """
        row = CURSOR.execute(sql, (cls.author_id)).fetchone()
        return cls.find_by_id(row) if row else None

    @classmethod
    def get_magazine(cls, magazine_id):
        sql = """ 
            SELECT * FROM magazines
            INNER JOIN articles
            ON magazines.id = articles.magazines_id
        """
        row = CURSOR.execute(sql, (cls.magazine_id)).fetchone()
        return cls.find_by_id(row) if row else None
    

    def __repr__(self):
        return f'<Article {self.title}>'
    
    @classmethod
    def instance_from_db(cls, row):
        return cls(row[0], row[1], row[2], row[3], row[4])
    
    def articles(self):
        sql = """ 
            SELECT articles.* 
            FROM articles 
            INNER JOIN authors 
            ON articles.author_id = authors.id 
            WHERE authors.id = ?
        """
        rows = CURSOR.execute(sql, (self.author_id,)).fetchall()
        return [self.instance_from_db(row) for row in rows]
    
    def magazines(self):
        # Use SQL JOIN to get all magazines associated with the author
        sql = """ 
            SELECT magazines.* 
            FROM magazines 
            INNER JOIN authors 
            ON magazines.author_id = authors.id 
            WHERE authors.id = ?
        """
        rows = CURSOR.execute(sql, (self.author_id,)).fetchall()
        return [self.instance_from_db(row) for row in rows]

#article = Article(1, "Test Title", "Test Content", 1, 1)
