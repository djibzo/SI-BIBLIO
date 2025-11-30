import datetime
from models.user import User
from models.book import Book

class NotificationService:
    def send_borrow_confirmation(self, user: User, book: Book, due_date: datetime.datetime):
        print(f"Email sent to {user.name}: Book '{book.title}' borrowed until {due_date.strftime('%Y-%m-%d')}")

    def send_penalty_notice(self, user: User, penalty: float):
        print(f"Email sent to {user.name}: Penalty of {penalty:.2f}€ applied")