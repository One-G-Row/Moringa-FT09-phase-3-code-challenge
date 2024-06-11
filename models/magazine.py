#lib/author.py
#from database.connection import get_db_connection
from app import CURSOR, CONN

class Magazine:
    all = []
    def __init__(self, id, name, category, author):
        self.id = id
        self.name = name
        self.category = category
       

    def save(self):
        sql=""" 
        INSERT INTO magazines 
        VALUES(?, ?):
        INSERT INTO magazines
         """
        
        
        CURSOR.execute(sql, (self.id, self.name, self.category))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def save(cls, id, name, category):
        magazine = cls(id, name, category)
        magazine.save()
        return magazine


    @property
    def id(self):
        self._id = id

    @id.setter
    def id(self, id, article_id):
        if isinstance(id, article_id):
            self._id = article_id
        else: 
            raise TypeError("")
        
    @classmethod
    def find_by_id(cls, id):
        sql = """ 
        SELECT * FROM magazines
        WHERE id = ?
        """
    
        row = CURSOR.execute(sql).fetchall()
        return cls.instance_from_db(row) if row else None

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and 2 <= name >=16:
            self._name = name
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, category):
        if( isinstance(category, str) and category > 0):
            self._category = category
        else:
            raise TypeError("category must be type string")

    def articles(self):
        sql = """ 
        SELECT articles * FROM articles
        INNER JOIN magazines
        ON articles.magazine_id = magazines.id
        WHERE magazine_id = ?
        """

        row = CURSOR.execute(sql, (self.id))
        return self.instance_from_db(row) if row else None

    def contributors(self):
        sql =""" 
        SELECT authors * FROM authors
        INNER JOIN articles
        ON authors.id = articles.author_id
        WHERE articles.magaezine_id = ?
     """
        
        row = CURSOR.execute(sql, (self.id)).fetchall()
        return self.instance_from_db(row) if row else None

    @classmethod
    def article_titles(cls):
        sql = """ 
        SELECT articles.title * FROM articles
        INNER JOIN magazines
        ON articles.magazine_id = magazines.id
     """
        
        row = CURSOR.execute(sql).fetchall()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def contributing_authors(cls, Author):
        sql = """ 
        SELECT authors * FROM authors
        INNER JOIN articles
        ON authors.id = articles.authors_id
        WHERE articles.magazine_id = ?
        WHERE COUNT > 2
     """
        row = CURSOR.execute(sql).fetchall()
        return [Author.instance_from_db(row) if row else None]
    
    def __repr__(self):
        return f'<Magazine {self.name}>'

magazine = Magazine(1, "Tech Weekly")