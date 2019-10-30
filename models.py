from app import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    author = db.Column(db.String())
    published = db.Column(db.String())
    createdOn = db.Column(db.String())

    def __init__(self, name, author, published, createdOn):
        self.name = name
        self.author = author
        self.published = published
        self.createdOn = createdOn

    def __repr__(self):
        return('<id> {}'.format(self.id))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'published': self.published,
            'createdOn': self.createdOn
        }


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    bookId = db.Column(db.Integer)
    content = db.Column(db.String())
    createdOn = db.Column(db.String())
    createdBy = db.Column(db.String())

    def __init__(self, bookId, content, createdOn, createdBy):
        self.bookId = bookId
        self.content = content
        self.createdOn = createdOn
        self.createdBy = createdBy
    
    def __repr__(self):
        return('<id> {}'.format(self.id))
    
    def serialize(self):
        return{
            bookId: self.bookId,
            content: self.content,
            createdOn: self.createdOn,
            createdBy: self.createdBy
        }