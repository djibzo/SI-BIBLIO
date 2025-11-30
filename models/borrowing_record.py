import datetime

class BorrowingRecord:
    def __init__(self, book_isbn: str, user_id: str, due_date: datetime.datetime):
        self.book_isbn = book_isbn
        self.user_id = user_id
        self.due_date = due_date