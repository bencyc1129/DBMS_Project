'''
Backend entry
'''
from fastapi import FastAPI, Depends
import models, schemas
from db import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind = engine) # create db tables

# funtion for getting db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI() # create web app object

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
@app.post("/inputSQL")
def index(SQL: schemas.SQLQuery, connection: Session = Depends(get_db)):
    splitedSQL = SQL.SQL.split(' ') # split raw sql into list
    op = splitedSQL[0].lower() # get the type of sql
    
    if op == 'delete': # DELETE FROM tablename WHERE col=...
                       # DELETE * FROM tablename (x, no such syntax)
                       # DELETE FROM tablename
        connection.execute(SQL.SQL)
        connection.commit()
        targetTable = splitedSQL[2]
        tableData, tableKeys = returnResultTable("SELECT * FROM " + targetTable + ";", connection)
        return schemas.queryResult(data = tableData, key = tableKeys)

    elif op == 'insert': # INSERT INTO tablename (col1, col2, ...) VALUES (val1, val2, ...)
        connection.execute(SQL.SQL)
        connection.commit()
        targetTable = splitedSQL[2]
        tableData, tableKeys = returnResultTable("SELECT * FROM " + targetTable + ";", connection)
        return schemas.queryResult(data = tableData, key = tableKeys)

    elif op == 'update': # UPDATE tablename SET col=... WHERE col=... 
        connection.execute(SQL.SQL)
        connection.commit()
        targetTable = splitedSQL[1]
        tableData, tableKeys = returnResultTable("SELECT * FROM " + targetTable + ";", connection)
        return schemas.queryResult(data = tableData, key = tableKeys)

    else: 
        tableData, tableKeys = returnResultTable(SQL.SQL, connection)
        return schemas.queryResult(data = tableData, key = tableKeys)

# get query result, and wrap it into schema obejct
def returnResultTable(SQL: str, connection: Session):
    result = connection.execute(SQL)
    mappedResult = result.mappings()
    tableData = []
    for data in mappedResult.all():
        items = dict(data).values()
        tableData.append(list(items))
    tableKeys = list(mappedResult.keys())
    
    return tableData, tableKeys 

# for testing
@app.get("/initialize", tags = ["test"])
def addAll(connection: Session = Depends(get_db)):
    # drop all tables
    connection.execute("drop table borrow;")
    connection.execute("drop table collect;")
    connection.execute("drop table register;")
    connection.execute("drop table publish;")
    connection.execute("drop table visit;")
    connection.execute("drop table author;")
    connection.execute("drop table book;")
    connection.execute("drop table publisher;")
    connection.execute("drop table library;")
    connection.execute("drop table user;")
    connection.commit()
    models.Base.metadata.create_all(bind = engine) # create db tables

    # insert data
    authors = [
        models.Author(authorId = 1, authorName = "東野圭吾", authorGender = "M", authorBirth = "1958-02-04"),
        models.Author(authorId = 2, authorName = "乙一", authorGender = "M", authorBirth = "1978-10-21"),
        models.Author(authorId = 3, authorName = "大澤在昌", authorGender = "M", authorBirth = "1956-03-08"),
        models.Author(authorId = 4, authorName = "湊佳苗", authorGender = "F", authorBirth = "1973-01-19"),
        models.Author(authorId = 5, authorName = "宮部美幸", authorGender = "F", authorBirth = "1960-12-23"),
        models.Author(authorId = 6, authorName = "Jeffery Deaver", authorGender = "M", authorBirth = "1950-05-06"),
        models.Author(authorId = 7, authorName = "Thomas Harris", authorGender = "M", authorBirth = "1940-09-22"),
        models.Author(authorId = 8, authorName = "Stephen Edwin King", authorGender = "M", authorBirth = "1947-09-21"),
        models.Author(authorId = 9, authorName = "Karl Stig-Erland Stieg Larsson", authorGender = "M", authorBirth = "1954-08-15"),
        models.Author(authorId = 10, authorName = "Joanne Rowling", authorGender = "F", authorBirth = "1965-07-31"),
    ]
    connection.add_all(authors)
    connection.commit()

    books = [
        models.Book(bookIsbn = "9784087744002", bookName = "白夜行", bookLang = "jp"),
        models.Book(bookIsbn = "9784163238609", bookName = "容疑者Xの献身", bookLang = "jp"),
        models.Book(bookIsbn = "9784041101360", bookName = "ナミヤ雑貨店の奇蹟", bookLang = "jp"),
        models.Book(bookIsbn = "9784087471984", bookName = "夏と花火と私の死体", bookLang = "jp"),
        models.Book(bookIsbn = "9784044253011", bookName = "失踪HOLIDAY", bookLang = "jp"),
        models.Book(bookIsbn = "9784334766986", bookName = "新宿鮫", bookLang = "jp"),
        models.Book(bookIsbn = "9784334767174", bookName = "毒猿", bookLang = "jp"),
        models.Book(bookIsbn = "9784575236286", bookName = "告白", bookLang = "jp"),
        models.Book(bookIsbn = "9784087714593", bookName = "白ゆき姫殺人事件", bookLang = "jp"),
        models.Book(bookIsbn = "978409379264X", bookName = "模倣犯 上", bookLang = "jp"),
        models.Book(bookIsbn = "9784093792658", bookName = "模倣犯 下", bookLang = "jp"),
        models.Book(bookIsbn = "9780340992722", bookName = "The Bone Collector", bookLang = "en"),
        models.Book(bookIsbn = "9781455517107", bookName = "The Skin Collector", bookLang = "en"),
        models.Book(bookIsbn = "9780312924584", bookName = "The Silence of the Lambs", bookLang = "en"),
        models.Book(bookIsbn = "9780440224679", bookName = "Hannibal", bookLang = "en"),
        models.Book(bookIsbn = "9780385121675", bookName = "The Shining", bookLang = "en"),
        models.Book(bookIsbn = "9780670813028", bookName = "It", bookLang = "en"),
        models.Book(bookIsbn = "9789113014081", bookName = "The Girl with the Dragon Tattoo", bookLang = "sv"),
        models.Book(bookIsbn = "9781847245564", bookName = "The Girl Who Played with Fire", bookLang = "sv"),
        models.Book(bookIsbn = "9780747532743", bookName = "Harry Potter and the Philosopher's Stone", bookLang = "en"),
        models.Book(bookIsbn = "9780439064866", bookName = "Harry Potter and the Chamber of Secrets", bookLang = "en"),
        models.Book(bookIsbn = "9780439136365", bookName = "Harry Potter and the Prisoner of Azkaban", bookLang = "en"),
        models.Book(bookIsbn = "9780747546245", bookName = "Harry Potter and the Goblet of Fire", bookLang = "en"),
        models.Book(bookIsbn = "9780439358071", bookName = "Harry Potter and the Order of the Phoenix", bookLang = "en"),
        models.Book(bookIsbn = "9780439785969", bookName = "Harry Potter and the Half-Blood Prince", bookLang = "en"),
        models.Book(bookIsbn = "9780747591054", bookName = "Harry Potter and the Deathly Hallows", bookLang = "en"),
    ]
    connection.add_all(books)
    connection.commit()

    publishers = [
        models.Publisher(publisherId = 1, publisherName = "集英社", publisherRepresent = "堀內丸恵", publisherNation = "Japan"),
        models.Publisher(publisherId = 2, publisherName = "文藝春秋", publisherRepresent = "松井清人", publisherNation = "Japan"),
        models.Publisher(publisherId = 3, publisherName = "角川書店", publisherRepresent = "堀內大示", publisherNation = "Japan"),
        models.Publisher(publisherId = 4, publisherName = "角川スニーカー文庫", publisherRepresent = "堀內大示", publisherNation = "Japan"),
        models.Publisher(publisherId = 5, publisherName = "光文社", publisherRepresent = "武田真士男", publisherNation = "Japan"),
        models.Publisher(publisherId = 6, publisherName = "双葉社", publisherRepresent = "戸塚源久", publisherNation = "Japan"),
        models.Publisher(publisherId = 7, publisherName = "株式会社小学館", publisherRepresent = "相賀昌宏", publisherNation = "Japan"),
        models.Publisher(publisherId = 8, publisherName = "Viking Press", publisherRepresent = "Brian Tart", publisherNation = "USA"),
        models.Publisher(publisherId = 9, publisherName = "Grand Central Publishing", publisherRepresent = "Michael Pietsch", publisherNation = "USA"),
        models.Publisher(publisherId = 10, publisherName = "St. Martin's Press", publisherRepresent = "George Witte", publisherNation = "USA"),
        models.Publisher(publisherId = 11, publisherName = "Doubleday", publisherRepresent = "Frank Doubleday", publisherNation = "USA"),
        models.Publisher(publisherId = 12, publisherName = "Norstedts förlag", publisherRepresent = "Per Adolf Norstedt", publisherNation = "Sweden"),
        models.Publisher(publisherId = 13, publisherName = "Bloomsbury Publishing plc", publisherRepresent = "Nigel Newton", publisherNation = "UK"),
    ]
    connection.add_all(publishers)
    connection.commit()

    publish = [
        models.Publish(author_id = 1, book_isbn = "9784087744002", publisher_id = 1),
        models.Publish(author_id = 1, book_isbn = "9784163238609", publisher_id = 2),
        models.Publish(author_id = 1, book_isbn = "9784041101360", publisher_id = 3),
        models.Publish(author_id = 2, book_isbn = "9784087471984", publisher_id = 1),
        models.Publish(author_id = 2, book_isbn = "9784044253011", publisher_id = 4),
        models.Publish(author_id = 3, book_isbn = "9784334766986", publisher_id = 5),
        models.Publish(author_id = 3, book_isbn = "9784334767174", publisher_id = 5),
        models.Publish(author_id = 4, book_isbn = "9784575236286", publisher_id = 6),
        models.Publish(author_id = 4, book_isbn = "9784087714593", publisher_id = 1),
        models.Publish(author_id = 5, book_isbn = "978409379264X", publisher_id = 7),
        models.Publish(author_id = 5, book_isbn = "9784093792658", publisher_id = 7),
        models.Publish(author_id = 6, book_isbn = "9780340992722", publisher_id = 8),
        models.Publish(author_id = 6, book_isbn = "9781455517107", publisher_id = 9),
        models.Publish(author_id = 7, book_isbn = "9780312924584", publisher_id = 10),
        models.Publish(author_id = 7, book_isbn = "9780440224679", publisher_id = 10),
        models.Publish(author_id = 8, book_isbn = "9780385121675", publisher_id = 11),
        models.Publish(author_id = 8, book_isbn = "9780670813028", publisher_id = 8),
        models.Publish(author_id = 9, book_isbn = "9789113014081", publisher_id = 12),
        models.Publish(author_id = 9, book_isbn = "9781847245564", publisher_id = 12),
        models.Publish(author_id = 10, book_isbn = "9780747532743", publisher_id = 13),
        models.Publish(author_id = 10, book_isbn = "9780439064866", publisher_id = 13),
        models.Publish(author_id = 10, book_isbn = "9780439136365", publisher_id = 13),
        models.Publish(author_id = 10, book_isbn = "9780747546245", publisher_id = 13),
        models.Publish(author_id = 10, book_isbn = "9780439358071", publisher_id = 13),
        models.Publish(author_id = 10, book_isbn = "9780439785969", publisher_id = 13),
        models.Publish(author_id = 10, book_isbn = "9780747591054", publisher_id = 13),
    ]
    connection.add_all(publish)
    connection.commit()

    libraries = [
        models.Library(libraryId = 1, libraryName = "國立成功大學圖書館", libraryPhone = "06 275 7575#65760", libraryAddress = "704台南市東區大學路1號"),
        models.Library(libraryId = 2, libraryName = "國立成功大學新K館", libraryPhone = "06 275 7575#65767", libraryAddress = "704台南市北區長榮路四段20號"),
        models.Library(libraryId = 3, libraryName = "國立台灣大學圖書館", libraryPhone = "02 3366 2326", libraryAddress = "106台北市大安區羅斯福路四段1號"),
        models.Library(libraryId = 4, libraryName = "國立陽明交通大學浩然圖書館", libraryPhone = "03 571 2121", libraryAddress = "300新竹市東區大學路1001號"),
        models.Library(libraryId = 5, libraryName = "國立清華大學圖書館", libraryPhone = "03 574 2995", libraryAddress = "300新竹市東區光復路二段101號"),
        models.Library(libraryId = 6, libraryName = "臺中市立圖書館總館", libraryPhone = "04 2422 9833", libraryAddress = "406台中市北屯區豐樂路二段158號"),
        models.Library(libraryId = 7, libraryName = "臺中市立圖書館大里分館", libraryPhone = "04 2496 2169", libraryAddress = "412台中市大里區中興路一段163號"),
        models.Library(libraryId = 8, libraryName = "臺中市立圖書館南區分館", libraryPhone = "04 2262 3497", libraryAddress = "402台中市南區五權南路335號"),
        models.Library(libraryId = 9, libraryName = "臺中市立圖書館南屯分館", libraryPhone = "04 2253 3836", libraryAddress = "408台中市南屯區大墩十二街361號"),
        models.Library(libraryId = 10, libraryName = "臺中市立圖書館中區分館", libraryPhone = "04 2225 2462", libraryAddress = "400台中市中區成功路300號7樓"),
    ]
    connection.add_all(libraries)
    connection.commit()

    collect = [
        models.Collect(book_isbn = "9784087744002", library_id = 1, num = 1),
        models.Collect(book_isbn = "9784163238609", library_id = 1, num = 3),
        models.Collect(book_isbn = "9784041101360", library_id = 1, num = 4),
        models.Collect(book_isbn = "9784087744002", library_id = 2, num = 7),
        models.Collect(book_isbn = "9784163238609", library_id = 2, num = 1),
        models.Collect(book_isbn = "9784041101360", library_id = 2, num = 2),
        models.Collect(book_isbn = "9784087471984", library_id = 3, num = 1),
        models.Collect(book_isbn = "9784044253011", library_id = 3, num = 1),
        models.Collect(book_isbn = "9784087471984", library_id = 4, num = 1),
        models.Collect(book_isbn = "9784044253011", library_id = 4, num = 3),
        models.Collect(book_isbn = "9784334766986", library_id = 5, num = 1),
        models.Collect(book_isbn = "9784334767174", library_id = 5, num = 5),
        models.Collect(book_isbn = "9784334766986", library_id = 6, num = 1),
        models.Collect(book_isbn = "9784334767174", library_id = 6, num = 1),
        models.Collect(book_isbn = "9784575236286", library_id = 7, num = 3),
        models.Collect(book_isbn = "9784087714593", library_id = 7, num = 1),
        models.Collect(book_isbn = "9784575236286", library_id = 8, num = 5),
        models.Collect(book_isbn = "9784087714593", library_id = 8, num = 1),
        models.Collect(book_isbn = "978409379264X", library_id = 9, num = 1),
        models.Collect(book_isbn = "9784093792658", library_id = 9, num = 6),
        models.Collect(book_isbn = "978409379264X", library_id = 10, num = 1),
        models.Collect(book_isbn = "9784093792658", library_id = 10, num = 9),
        models.Collect(book_isbn = "9780340992722", library_id = 1, num = 1),
        models.Collect(book_isbn = "9781455517107", library_id = 1, num = 1),
        models.Collect(book_isbn = "9780340992722", library_id = 3, num = 1),
        models.Collect(book_isbn = "9781455517107", library_id = 3, num = 8),
        models.Collect(book_isbn = "9780312924584", library_id = 5, num = 6),
        models.Collect(book_isbn = "9780440224679", library_id = 5, num = 1),
        models.Collect(book_isbn = "9780312924584", library_id = 7, num = 1),
        models.Collect(book_isbn = "9780440224679", library_id = 7, num = 1),
        models.Collect(book_isbn = "9780385121675", library_id = 9, num = 4),
        models.Collect(book_isbn = "9780670813028", library_id = 9, num = 1),
        models.Collect(book_isbn = "9780385121675", library_id = 2, num = 1),
        models.Collect(book_isbn = "9780670813028", library_id = 2, num = 3),
        models.Collect(book_isbn = "9789113014081", library_id = 4, num = 1),
        models.Collect(book_isbn = "9781847245564", library_id = 4, num = 2),
        models.Collect(book_isbn = "9789113014081", library_id = 6, num = 1),
        models.Collect(book_isbn = "9781847245564", library_id = 6, num = 1),

        models.Collect(book_isbn = "9780747532743", library_id = 1, num = 3),
        models.Collect(book_isbn = "9780439064866", library_id = 1, num = 1),
        models.Collect(book_isbn = "9780439136365", library_id = 1, num = 3),
        models.Collect(book_isbn = "9780747546245", library_id = 1, num = 7),
        models.Collect(book_isbn = "9780439358071", library_id = 1, num = 9),
        models.Collect(book_isbn = "9780439785969", library_id = 1, num = 3),
        models.Collect(book_isbn = "9780747591054", library_id = 1, num = 0),

        models.Collect(book_isbn = "9780747532743", library_id = 3, num = 3),
        models.Collect(book_isbn = "9780439064866", library_id = 3, num = 3),
        models.Collect(book_isbn = "9780439136365", library_id = 3, num = 3),
        models.Collect(book_isbn = "9780747546245", library_id = 3, num = 2),
        models.Collect(book_isbn = "9780439358071", library_id = 3, num = 3),
        models.Collect(book_isbn = "9780439785969", library_id = 3, num = 1),
        models.Collect(book_isbn = "9780747591054", library_id = 3, num = 3),

        models.Collect(book_isbn = "9780747532743", library_id = 4, num = 3),
        models.Collect(book_isbn = "9780439064866", library_id = 4, num = 3),
        models.Collect(book_isbn = "9780439136365", library_id = 4, num = 3),
        models.Collect(book_isbn = "9780747546245", library_id = 4, num = 2),
        models.Collect(book_isbn = "9780439358071", library_id = 4, num = 3),
        models.Collect(book_isbn = "9780439785969", library_id = 4, num = 5),
        models.Collect(book_isbn = "9780747591054", library_id = 4, num = 7),

        models.Collect(book_isbn = "9780747532743", library_id = 5, num = 3),
        models.Collect(book_isbn = "9780439064866", library_id = 5, num = 3),
        models.Collect(book_isbn = "9780439136365", library_id = 5, num = 3),
        models.Collect(book_isbn = "9780747546245", library_id = 5, num = 4),
        models.Collect(book_isbn = "9780439358071", library_id = 5, num = 9),
        models.Collect(book_isbn = "9780439785969", library_id = 5, num = 3),
        models.Collect(book_isbn = "9780747591054", library_id = 5, num = 10),
    ]
    connection.add_all(collect)
    connection.commit()

    users = [
        models.User(userId = 1, userName = "Ben", userPhone = "0916295998"),
        models.User(userId = 2, userName = "Alex", userPhone = "0972648298"),
        models.User(userId = 3, userName = "Jenny", userPhone = "0919326773"),
        models.User(userId = 4, userName = "Johnny", userPhone = "0988019793"),
        models.User(userId = 5, userName = "Amber", userPhone = "0934376787"),
        models.User(userId = 6, userName = "John", userPhone = "0954545335"),
        models.User(userId = 7, userName = "Ann", userPhone = "0916860642"),
        models.User(userId = 8, userName = "Zac", userPhone = "0958132436"),
        models.User(userId = 9, userName = "Peter", userPhone = "0987421024"),
        models.User(userId = 10, userName = "Melody", userPhone = "0937632773"),
    ]
    connection.add_all(users)
    connection.commit()

    register = [
        models.Register(user_id = 1, library_id = 1, startDate = "2019-01-12", point = 100),
        models.Register(user_id = 1, library_id = 2, startDate = "2019-05-12", point = 0),
        models.Register(user_id = 2, library_id = 2, startDate = "2019-07-30", point = 50),
        models.Register(user_id = 2, library_id = 3, startDate = "2019-02-10", point = 200),
        models.Register(user_id = 3, library_id = 3, startDate = "2019-11-10", point = 75),
        models.Register(user_id = 3, library_id = 4, startDate = "2019-11-19", point = 20),
        models.Register(user_id = 4, library_id = 4, startDate = "2019-07-01", point = 1000),
        models.Register(user_id = 4, library_id = 5, startDate = "2019-07-08", point = 250),
        models.Register(user_id = 4, library_id = 6, startDate = "2019-07-23", point = 70),
        models.Register(user_id = 5, library_id = 5, startDate = "2019-10-12", point = 80),
        models.Register(user_id = 5, library_id = 6, startDate = "2019-10-30", point = 85),
        models.Register(user_id = 6, library_id = 6, startDate = "2019-03-17", point = 900),
        models.Register(user_id = 7, library_id = 7, startDate = "2019-08-18", point = 10),
        models.Register(user_id = 8, library_id = 8, startDate = "2019-03-13", point = 5),
        models.Register(user_id = 9, library_id = 9, startDate = "2019-08-28", point = 100),
        models.Register(user_id = 10, library_id = 10, startDate = "2019-01-10", point = 100),
    ]
    connection.add_all(register)
    connection.commit()

    visit = [
        models.Visit(user_id = 1, library_id = 1, visitDate = "2022-01-12"),
        models.Visit(user_id = 1, library_id = 2, visitDate = "2022-05-12"),
        models.Visit(user_id = 2, library_id = 2, visitDate = "2022-07-30"),
        models.Visit(user_id = 2, library_id = 3, visitDate = "2022-02-10"),
        models.Visit(user_id = 3, library_id = 3, visitDate = "2022-11-10"),
        models.Visit(user_id = 3, library_id = 4, visitDate = "2022-11-19"),
        models.Visit(user_id = 4, library_id = 4, visitDate = "2022-07-01"),
        models.Visit(user_id = 4, library_id = 5, visitDate = "2022-07-08"),
        models.Visit(user_id = 4, library_id = 6, visitDate = "2022-07-23"),
        models.Visit(user_id = 5, library_id = 5, visitDate = "2022-10-12"),
        models.Visit(user_id = 5, library_id = 6, visitDate = "2022-10-30"),
        models.Visit(user_id = 6, library_id = 6, visitDate = "2022-03-17"),
        models.Visit(user_id = 7, library_id = 7, visitDate = "2022-08-18"),
        models.Visit(user_id = 8, library_id = 8, visitDate = "2022-03-13"),
        models.Visit(user_id = 9, library_id = 9, visitDate = "2022-08-28"),
        models.Visit(user_id = 10, library_id = 10, visitDate = "2022-01-10"),
    ]
    connection.add_all(visit)
    connection.commit()

    borrow = [
        models.Borrow(user_id = 1, library_id = 1, book_isbn = "9784087744002"),
        models.Borrow(user_id = 1, library_id = 1, book_isbn = "9784163238609"),
        models.Borrow(user_id = 2, library_id = 2, book_isbn = "9780385121675"),
        models.Borrow(user_id = 3, library_id = 3, book_isbn = "9780439785969"),
        models.Borrow(user_id = 5, library_id = 4, book_isbn = "9780747532743"),
        models.Borrow(user_id = 5, library_id = 5, book_isbn = "9780440224679"),
        models.Borrow(user_id = 5, library_id = 6, book_isbn = "9781847245564"),
        models.Borrow(user_id = 7, library_id = 7, book_isbn = "9784575236286"),
        models.Borrow(user_id = 8, library_id = 8, book_isbn = "9784087714593"),
        models.Borrow(user_id = 9, library_id = 9, book_isbn = "9780670813028"),
        models.Borrow(user_id = 9, library_id = 10, book_isbn = "978409379264X"),
    ]
    connection.add_all(borrow)
    connection.commit()