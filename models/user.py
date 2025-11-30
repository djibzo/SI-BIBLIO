from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

    @property
    @abstractmethod
    def max_borrow_limit(self) -> int:
        pass

    @property
    @abstractmethod
    def borrow_duration_days(self) -> int:
        pass


class Student(User):
    @property
    def max_borrow_limit(self) -> int:
        return 3

    @property
    def borrow_duration_days(self) -> int:
        return 14


class Teacher(User):
    @property
    def max_borrow_limit(self) -> int:
        return 10

    @property
    def borrow_duration_days(self) -> int:
        return 30


class Staff(User):
    @property
    def max_borrow_limit(self) -> int:
        return 5

    @property
    def borrow_duration_days(self) -> int:
        return 21