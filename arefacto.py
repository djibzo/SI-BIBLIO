import datetime
import json


class Book:
   def __init__(self, isbn, title, author, available=True):
       self.isbn = isbn
       self.title = title
       self.author = author
       self.available = available
       self.borrowed_by = None
       self.due_date = None
  
   def borrow(self, student_id):
       if not self.available:
           return False
      
       self.available = False
       self.borrowed_by = student_id
       self.due_date = datetime.datetime.now() + datetime.timedelta(days=14)
      
       # Envoi d'email
       print(f"Email sent to student {student_id}: Book '{self.title}' borrowed until {self.due_date}")
      
       # Log dans un fichier
       with open('library.log', 'a') as f:
           f.write(f"{datetime.datetime.now()}: Book {self.isbn} borrowed by {student_id}\n")
      
       # Mise à jour de la base de données
       print(f"Database updated: Book {self.isbn} marked as borrowed")
      
       return True
  
   def return_book(self):
       if self.available:
           return False
          
       # Calcul des pénalités
       if datetime.datetime.now() > self.due_date:
           days_late = (datetime.datetime.now() - self.due_date).days
           penalty = days_late * 0.50  # 0.50€ par jour
           print(f"Penalty: {penalty}€ for {days_late} days late")
          
           # Envoi d'email de pénalité
           print(f"Email sent: Penalty of {penalty}€ applied")
      
       self.available = True
       old_borrower = self.borrowed_by
       self.borrowed_by = None
       self.due_date = None
      
       # Log
       with open('library.log', 'a') as f:
           f.write(f"{datetime.datetime.now()}: Book {self.isbn} returned by {old_borrower}\n")
      
       return True
  
   def to_json(self):
       return json.dumps({
           'isbn': self.isbn,
           'title': self.title,
           'author': self.author,
           'available': self.available,
           'borrowed_by': self.borrowed_by,
           'due_date': self.due_date.isoformat() if self.due_date else None
       })
  
   def to_xml(self):
       return f"""<book>
           <isbn>{self.isbn}</isbn>
           <title>{self.title}</title>
           <author>{self.author}</author>
           <available>{self.available}</available>
           <borrowed_by>{self.borrowed_by or ''}</borrowed_by>
           <due_date>{self.due_date.isoformat() if self.due_date else ''}</due_date>
       </book>"""


class User:
   def __init__(self, user_id, name, user_type):
       self.user_id = user_id
       self.name = name
       self.user_type = user_type  # 'student', 'teacher', 'staff'
       self.borrowed_books = []
  
   def can_borrow(self):
       if self.user_type == 'student' and len(self.borrowed_books) >= 3:
           return False
       elif self.user_type == 'teacher' and len(self.borrowed_books) >= 10:
           return False
       elif self.user_type == 'staff' and len(self.borrowed_books) >= 5:
           return False
       return True
  
   def get_borrow_duration(self):
       if self.user_type == 'student':
           return 14
       elif self.user_type == 'teacher':
           return 30
       elif self.user_type == 'staff':
           return 21
       return 14


class Library:
   def __init__(self):
       self.books = {}
       self.users = {}
  
   def add_book(self, book):
       self.books[book.isbn] = book
  
   def add_user(self, user):
       self.users[user.user_id] = user
  
   def search_books(self, search_type, query):
       results = []
      
       if search_type == 'title':
           for book in self.books.values():
               if query.lower() in book.title.lower():
                   results.append(book)
       elif search_type == 'author':
           for book in self.books.values():
               if query.lower() in book.author.lower():
                   results.append(book)
       elif search_type == 'isbn':
           for book in self.books.values():
               if query in book.isbn:
                   results.append(book)
      
       return results
  
   def generate_report(self, report_type):
       if report_type == 'borrowed':
           print("=== Borrowed Books Report ===")
           for book in self.books.values():
               if not book.available:
                   print(f"{book.title} - Borrowed by {book.borrowed_by}")
       elif report_type == 'available':
           print("=== Available Books Report ===")
           for book in self.books.values():
               if book.available:
                   print(f"{book.title} by {book.author}")
       elif report_type == 'overdue':
           print("=== Overdue Books Report ===")
           for book in self.books.values():
               if not book.available and book.due_date < datetime.datetime.now():
                   days_late = (datetime.datetime.now() - book.due_date).days
                   print(f"{book.title} - {days_late} days overdue")
