from enum import Enum
import csv
import itertools
from typing import List


class Subject(Enum):
    MATH = 'Математика'
    RUSSIAN_LANG = 'Русcкий Язык'
    FOREIGN_LANG = 'Английский Язык'
    HISTORY = "История"
    PHYSICS = "Физика"
    CHEMISTRY = "Химия"
    BIOLOGY = "Биология"
    SOCIAL_STUDIES = "Обществознание"
    INFORMATICS = "Информатика"
    TECHNOLOGY = "Технология"
    GEOGRAPHY = "География"


class Human:
    name: str
    last_name: str
    ids = set()
    id_counter = 1

    def __init__(self, name, last_name, id=None):
        self.name = name
        self.last_name = last_name
        self.__id = None

        if id is not None:
            if id in Human.ids:
                raise Exception("Переданный id уже существует!")
            self.__id = id
        else:
            while self.__id is None or self.__id in Human.ids:
                self.__id = Human.id_counter
                Human.id_counter += 1

        Human.ids.add(self.__id)

    def __lt__(self, other):
        return (self.last_name, self.name) < (other.last_name, other.name)

    def __hash__(self):
        return hash(self.__id)

    def __repr__(self):
        return f"Human({self.name}, {self.last_name}, id={self.__id})"

    def __str__(self):
        return f"{self.name} {self.last_name}"


class Class:
    def __init__(self, subject_teacher, students=[]):
        self.teacher = subject_teacher
        self.students = list(students)

    def add_student(self, pupil):
        self.students.append(pupil)

    def __getitem__(self, search_str):
        return [student for student in self.students if
                student.name.startswith(search_str) or student.last_name.startswith(search_str)]

    def __iter__(self):
        return iter(sorted(self.students))

    @staticmethod
    def write_csv(filename, students):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for student in students:
                writer.writerow([student.name, student.last_name, student.get_class()])

    @staticmethod
    def read_csv(filename):
        students = []
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                name, last_name, class_number = row
                students.append(Student(name, last_name, class_number))
        return students


class Student(Human):
    def __init__(self, name, last_name, class_number=None, id=None):
        super().__init__(name, last_name, id)
        self.class_number = class_number

    def set_class(self, class_number):
        self.class_number = class_number

    def get_class(self):
        return self.class_number


class Teacher(Human):
    _homeroom_class: Class | None
    _subjects: List[Subject]

    def __init__(self, name, last_name, subjects, id=None):
        super().__init__(name, last_name, id)
        self.subjects = subjects

    def set_class(self, class_number):
        self.class_number = class_number

    def get_class(self):
        return self.class_number


# Пример использования
if __name__ == "__main__":
    teacher = Teacher("Иван", "Иванов", ["Математика", "Физика"])
    student1 = Student("Алексей", "Петров", 10)
    student2 = Student("Мария", "Сидорова", 10)

    school_class = Class(teacher, [student1, student2])

    # Запись в CSV
    Class.write_csv('students.csv', school_class.students)

    # Чтение из CSV
    new_students = Class.read_csv('students.csv')
    new_class = Class(teacher, new_students)

    for student in new_class:
        print(student)
