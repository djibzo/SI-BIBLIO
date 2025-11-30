import datetime
from models.book import Book
from models.user import User

class LoggingService:
    def __init__(self, log_file='library.log'):
        self.log_file = log_file

    def log_borrow(self, book: Book, user: User):
        with open(self.log_file, 'a') as f:
            f.write(f"{datetime.datetime.now()}: Book {book.isbn} borrowed by {user.user_id}\n")

    def log_return(self, book: Book, user: User):
        with open(self.log_file, 'a') as f:
            f.write(f"{datetime.datetime.now()}: Book {book.isbn} returned by {user.user_id}\n")