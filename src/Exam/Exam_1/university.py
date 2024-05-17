from dataclasses import dataclass


class DoubleRegestration(Exception):
    pass


@dataclass(unsafe_hash=True)
class Person:
    name: str
    surname: str
    extra_id: int = 0


class Student(Person):
    def __init__(self, name: str, surname: str, extra_id: int = 0) -> None:
        super().__init__(name, surname, extra_id)


class Professor(Person):
    def __init__(self, name: str, surname: str, extra_id: int = 0) -> None:
        super().__init__(name, surname, extra_id)


class Subject:
    def __init__(self, title: str, week_count: int) -> None:
        self.title: str = title
        self.week_count: int = week_count
        self.grades: dict[Student, int] = dict()
        self.professors: list[Professor] = list()

    def sign_student(self, student: Student) -> None:
        if student in self.grades.keys():
            raise DoubleRegestration("This student already signed")
        self.grades[student] = 0

    def sign_professor(self, professor: Professor) -> None:
        if professor in self.professors:
            raise DoubleRegestration("This professor already signed")
        self.professors.append(professor)

    def set_grade(self, student: Student, grade: int) -> None:
        if student not in self.grades.keys():
            raise KeyError("There is no such student")
        self.grades[student] = grade

    def get_average_grade(self) -> float:
        grades = self.grades.values()
        if len(grades) == 0:
            return 0
        return sum(grades) / len(grades)


class University:
    def __init__(self, title: str) -> None:
        self.title: str = title
        self.professors: dict[Professor, set[str]] = dict()
        self.students: dict[Student, set[str]] = dict()
        self.subjects: dict[str, Subject] = dict()

    def add_student(self, name: str, surname: str, subject_list: list[str]) -> int:
        students = self.students.keys()
        student = Student(name, surname)
        extra_id = 0
        while student in students:
            student = Student(name, surname, extra_id + 1)
            extra_id += 1
        self.students[student] = set()
        for subject in subject_list:
            self.sign_student(subject, name, surname, extra_id)
        return extra_id

    def add_professor(self, name: str, surname: str, subject_list: list[str]) -> int:
        professors = self.professors.keys()
        professor = Professor(name, surname)
        extra_id = 0
        while professor in professors:
            professor = Professor(name, surname, extra_id + 1)
            extra_id += 1
        self.professors[professor] = set()
        for subject in subject_list:
            self.sign_professor(subject, name, surname, extra_id)
        return extra_id

    def sign_student(self, sub: str, name: str, surname: str, extra_id: int = 0) -> None:
        student = Student(name, surname, extra_id)
        subject = self.subjects.get(sub, None)
        if subject is None:
            raise KeyError("No such subject")
        subject.sign_student(student)
        self.students[student].add(sub)

    def sign_professor(self, sub: str, name: str, surname: str, extra_id: int = 0) -> None:
        professor = Professor(name, surname, extra_id)
        subject = self.subjects.get(sub, None)
        if subject is None:
            raise KeyError("No such subject")
        subject.sign_professor(professor)
        self.professors[professor].add(sub)

    def add_subject(self, title: str, week_count: int) -> None:
        subject = Subject(title, week_count)
        if title in self.subjects.keys():
            raise DoubleRegestration("This subject is already registered")
        self.subjects[title] = subject

    def get_professors_workload(self, name: str, surname: str, extra_id: int = 0) -> int:
        professor = Professor(name, surname, extra_id)
        if professor not in self.professors.keys():
            raise KeyError("No such professor")
        week_count = 0
        for sub in self.professors[professor]:
            week_count += self.subjects[sub].week_count
        return week_count

    def set_grade(self, grade: int, sub: str, name: str, surname: str, extra_id: int = 0) -> None:
        student = Student(name, surname, extra_id)
        if student not in self.students.keys():
            raise KeyError("No such student")
        if sub not in self.students[student] or sub not in self.subjects.keys():
            raise KeyError("No such subject")
        self.subjects[sub].set_grade(student, grade)

    def get_average_student(self, name: str, surname: str, extra_id: int = 0) -> float:
        student = Student(name, surname, extra_id)
        if student not in self.students.keys():
            raise KeyError("No such student")
        subjects = [self.subjects[sub] for sub in self.students[student]]
        grades = [sub.grades[student] for sub in subjects]
        return sum(grades) / len(grades)

    def get_average_sub(self, sub: str) -> float:
        if sub not in self.subjects.keys():
            raise KeyError("No such subject")
        return self.subjects[sub].get_average_grade()
