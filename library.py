import datetime

from models.book import Book
from models.user import User
from models.borrowing_record import BorrowingRecord
from services.notification_service import NotificationService
from services.logging_service import LoggingService

class Library:
    """SRP: Orchestrates all library operations. DIP: Depends on service abstractions."""
    def __init__(self, notification_service: NotificationService, logging_service: LoggingService):
        self.books = {}  # key: isbn, value: Book
        self.users = {}  # key: user_id, value: User
        self.borrowing_records = {} # key: isbn, value: BorrowingRecord
        # DIP: Injecting dependencies
        self.notification_service = notification_service
        self.logging_service = logging_service

    def add_book(self, book: Book):
        self.books[book.isbn] = book

    def add_user(self, user: User):
        self.users[user.user_id] = user

    def is_book_available(self, book_isbn: str) -> bool:
        return book_isbn not in self.borrowing_records

    def get_user_borrowed_count(self, user_id: str) -> int:
        return sum(1 for record in self.borrowing_records.values() if record.user_id == user_id)

    def borrow_book(self, user_id: str, book_isbn: str) -> bool:
        if book_isbn not in self.books or user_id not in self.users:
            return False # Book or user does not exist

        book = self.books[book_isbn]
        user = self.users[user_id]

        if not self.is_book_available(book_isbn):
            return False # Book not available

        if self.get_user_borrowed_count(user_id) >= user.max_borrow_limit:
            return False # User has reached borrow limit

        due_date = datetime.datetime.now() + datetime.timedelta(days=user.borrow_duration_days)
        self.borrowing_records[book_isbn] = BorrowingRecord(book_isbn, user_id, due_date)

        self.logging_service.log_borrow(book, user)
        self.notification_service.send_borrow_confirmation(user, book, due_date)
        print(f"Database updated: Book {book.isbn} marked as borrowed by {user.user_id}")
        return True

    def return_book(self, book_isbn: str) -> bool:
        if self.is_book_available(book_isbn):
            return False # Book was not borrowed

        record = self.borrowing_records[book_isbn]
        book = self.books[book_isbn]
        user = self.users[record.user_id]

        if datetime.datetime.now() > record.due_date:
            days_late = (datetime.datetime.now() - record.due_date).days
            penalty = days_late * 0.50
            print(f"Penalty: {penalty:.2f}€ for {days_late} days late")
            self.notification_service.send_penalty_notice(user, penalty)

        del self.borrowing_records[book_isbn]
        self.logging_service.log_return(book, user)
        print(f"Database updated: Book {book.isbn} marked as returned")
        return True