from library import Library
from models.book import Book
from models.user import Student, Teacher
from services.logging_service import LoggingService
from services.notification_service import NotificationService

def run_demo():
    """
    Fonction principale pour démontrer l'utilisation du système de bibliothèque.
    """
    print("--- Initialisation de la bibliothèque ---")

    # 1. Initialiser les services.
    notification_service = NotificationService()
    logging_service = LoggingService(log_file='library_activity.log')

    # 2. Initialiser la bibliothèque en lui passant les services (Injection de Dépendance).
    my_library = Library(
        notification_service=notification_service,
        logging_service=logging_service
    )

    # 3. Créer et ajouter des livres et des utilisateurs.
    print("\n--- Ajout des données initiales ---")
    book1 = Book("978-0321765723", "The C++ Programming Language", "Bjarne Stroustrup")
    book2 = Book("978-0134685991", "Effective Modern C++", "Scott Meyers")
    book3 = Book("978-0262033848", "Introduction to Algorithms", "Thomas H. Cormen")
    book4 = Book("978-1491904244", "You Don't Know JS: Up & Going", "Kyle Simpson")

    student1 = Student(user_id="S001", name="Alice")
    teacher1 = Teacher(user_id="T001", name="Bob")

    my_library.add_book(book1)
    my_library.add_book(book2)
    my_library.add_book(book3)
    my_library.add_book(book4)
    my_library.add_user(student1)
    my_library.add_user(teacher1)
    print("Livres et utilisateurs ajoutés à la bibliothèque.")

    # 4. Scénarios d'utilisation.
    print("\n--- Scénario 1: Emprunt réussi par un étudiant ---")
    my_library.borrow_book(user_id="S001", book_isbn="978-0321765723")

    print("\n--- Scénario 2: Tentative d'emprunt du même livre (déjà emprunté) ---")
    success = my_library.borrow_book(user_id="T001", book_isbn="978-0321765723")
    if not success:
        print("Échec de l'emprunt,livre n'est pas disponible.")

    print("\n--- Scénario 3: L'étudiant atteint sa limite d'emprunts (limite de 3) ---")
    my_library.borrow_book(user_id="S001", book_isbn="978-0134685991")
    my_library.borrow_book(user_id="S001", book_isbn="978-0262033848")
    
    print("\nTentative d'emprunt d'un 4ème livre par l'étudiant:")
    success = my_library.borrow_book(user_id="S001", book_isbn="978-1491904244")
    if not success:
        print("Échec de l'emprunt, comme prévu, car la limite est atteinte.")

    print("\n--- Scénario 4: Retour d'un livre ---")
    my_library.return_book(book_isbn="978-0321765723")
    print(f"Le livre '{book1.title}' a été retourné.")


if __name__ == "__main__":
    run_demo()