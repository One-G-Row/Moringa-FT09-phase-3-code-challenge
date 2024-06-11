#lib/author.py
from app import CURSOR, CONN
#from database.connection import get_db_connection

class Author:
    all = []
    def __init__(self, id, name):
        self.id = id
        self._name = name
        #self.author_id = author_id
    
    def save(self):
        sql = """ 
        INSERT INTO authors(id, name)
        VALUES(?, ?)
        """

        CURSOR.execute(sql, (self.id, self.name))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
    
    @classmethod
    def create(cls, id, name):
        author = cls(name, id)
        author.save()
        return author


    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if isinstance(int, id):
            self._id = id
        else: 
            raise TypeError("id must be of type int")
        
    @classmethod
    def find_by_name(cls, name):
        sql = """ 
            SELECT *
            FROM authors
            WHERE name is ?
         """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else: 
            raise TypeError("names must be of type string")

    def articles(self):
        sql = """ 
        SELECT articles * FROM articles
        INNER JOIN authors
        ON articles.author_id = authors.id
        WHERE author_id = ?
     """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [self.instance_from_db(row) for row in rows]

    def magazines(self):
        sql = """ 
        SELECT magazines * FROM magazines
        INNER JOIN authors
        ON magazines.id = authors.magazine_id
        WHERE magazine_id = ?
     """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [self.instance_from_db(row) for row in rows]

    def __repr__(self):
        return f'<Author {self.name}>'

author = Author(1, "John Doe")