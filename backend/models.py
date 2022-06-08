'''
DB table definition
'''
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKeyConstraint
from db import Base

# relationships
class Collect(Base):
    __tablename__ = "collect"
    book_isbn = Column(String(256), ForeignKey("book.bookIsbn", ondelete="CASCADE"), primary_key = True)
    library_id = Column(Integer, ForeignKey("library.libraryId", ondelete="CASCADE"), primary_key = True)
    num = Column(Integer, nullable = False)

class Register(Base):
    __tablename__ = "register"
    user_id = Column(Integer, ForeignKey("user.userId", ondelete="CASCADE"), primary_key = True)
    library_id = Column(Integer, ForeignKey("library.libraryId", ondelete="CASCADE"), primary_key = True)
    startDate = Column(Date, nullable = False)
    point = Column(Integer, nullable = False)

class Borrow(Base):
    __tablename__ = "borrow"
    user_id = Column(Integer, ForeignKey("user.userId", ondelete="CASCADE"), primary_key = True)
    library_id = Column(Integer, ForeignKey("collect.library_id", ondelete="CASCADE"), primary_key = True)
    book_isbn = Column(String(256), ForeignKey("collect.book_isbn", ondelete="CASCADE"), primary_key = True)
    __table_args__ = (
        ForeignKeyConstraint(
            [library_id, book_isbn],
            [Collect.library_id, Collect.book_isbn]
        ), {}
    )

    user = relationship("User", back_populates = "borrow", cascade = "all, delete")

class Visit(Base):
    __tablename__ = "visit"
    user_id = Column(Integer, ForeignKey("user.userId", ondelete="CASCADE"), primary_key = True)
    library_id = Column(Integer, ForeignKey("library.libraryId", ondelete="CASCADE"), primary_key = True)
    visitDate = Column(Date, nullable = False)

class Publish(Base):
    __tablename__ = "publish"
    author_id = Column(Integer, ForeignKey("author.authorId", ondelete="CASCADE"), primary_key = True)
    book_isbn = Column(String(256), ForeignKey("book.bookIsbn", ondelete="CASCADE"), primary_key = True)
    publisher_id = Column(Integer, ForeignKey("publisher.publisherId", ondelete="CASCADE"), primary_key = True)

    author = relationship("Author", back_populates = "publish", cascade = "all, delete")
    book = relationship("Book", back_populates = "publish", cascade = "all, delete")
    publisher = relationship("Publisher", back_populates = "publish", cascade = "all, delete")

# entities
class Book(Base):
    __tablename__ = "book"
    bookIsbn = Column(String(256), primary_key = True)
    bookName = Column(String(256), nullable = False)
    bookLang = Column(String(256), nullable = False)
    collectLibraries = relationship("Library", secondary = "collect", back_populates = "collectBooks", passive_deletes = True)
    publish = relationship("Publish", back_populates = "book", passive_deletes = True)

class Author(Base):
    __tablename__ = "author"
    authorId = Column(Integer, primary_key = True)
    authorName = Column(String(256), nullable = False)
    authorGender = Column(String(256), nullable = False)
    authorBirth = Column(Date, nullable = False)
    publish = relationship("Publish", back_populates = "author", passive_deletes = True)

class Publisher(Base):
    __tablename__ = "publisher"
    publisherId = Column(Integer, primary_key = True)
    publisherName = Column(String(256), nullable = False)
    publisherRepresent = Column(String(256), nullable = False)
    publisherNation = Column(String(256), nullable = False)
    publish = relationship("Publish", back_populates = "publisher", passive_deletes = True)

class Library(Base):
    __tablename__ = "library"
    libraryId = Column(Integer, primary_key = True)
    libraryName = Column(String(256), nullable = False)
    libraryPhone = Column(String(256), nullable = False)
    libraryAddress = Column(String(256), nullable = False)
    collectBooks = relationship("Book", secondary = "collect", back_populates = "collectLibraries", cascade = "all, delete")
    registerusers = relationship("User", secondary = "register", back_populates = "registerLibraries", cascade = "all, delete")
    visitusers = relationship("User", secondary = "visit", back_populates = "visitLibraries", cascade = "all, delete")

class User(Base):
    __tablename__ = "user"
    userId = Column(Integer, primary_key = True)
    userName = Column(String(256), nullable = False)
    userPhone = Column(String(256), nullable = False)
    registerLibraries = relationship("Library", secondary = "register", back_populates = "registerusers", passive_deletes=True)
    borrow = relationship("Borrow", back_populates = "user", passive_deletes=True)
    visitLibraries = relationship("Library", secondary = "visit", back_populates = "visitusers", passive_deletes=True)