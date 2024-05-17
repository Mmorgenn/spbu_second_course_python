import pytest

from src.Exam.Exam_1.university import DoubleRegestration, Professor, Student, University


class Tester:
    def __init__(self):
        self.university = University("SPBU")

    def add_students(self, students):
        for name, surname, subjects in students:
            self.university.add_student(name, surname, subjects)

    def add_professor(self, professors):
        for name, surname, subjects in professors:
            self.university.add_professor(name, surname, subjects)

    def add_subjects(self, subjects):
        for title, week_count in subjects:
            self.university.add_subject(title, week_count)

    def set_grades(self, students):
        for grade, sub, name, surname, extra_id in students:
            self.university.set_grade(grade, sub, name, surname, extra_id)

    def add_sub_case(self):
        self.add_subjects((("Math", 12), ("English", 14), ("Russian", 8), ("Physic", 20), ("Chemistry", 10)))

    def add_students_case(self):
        self.add_students(
            (
                ("Bob", "Bobov", ["Math", "English"]),
                ("Ben", "Benedict", ["Physic", "Chemistry"]),
                ("Maksim", "Popov", ["Math", "Russian", "English"]),
                ("Andrew", "Tate", ["English"]),
                ("Ivan", "Hope", ["Math", "English"]),
            )
        )

    def add_professor_case(self):
        self.add_professor(
            (
                ("Anton", "Antonov", ["Math", "Physic"]),
                ("Boris", "Bobikov", ["Russian", "English"]),
                ("Maksim", "Popov", []),
                ("Nikita", "Volkov", ["English", "Russian", "Chemistry", "Math"]),
                ("Kate", "Kane", ["Physic"]),
            )
        )

    def set_grades_case(self):
        self.set_grades(
            (
                (4, "Math", "Bob", "Bobov", 0),
                (5, "English", "Bob", "Bobov", 0),
                (5, "Physic", "Ben", "Benedict", 0),
                (2, "Math", "Maksim", "Popov", 0),
                (4, "English", "Maksim", "Popov", 0),
                (5, "Russian", "Maksim", "Popov", 0),
                (6, "English", "Andrew", "Tate", 0),
            )
        )


@pytest.mark.parametrize(
    "subjects,expected", (((("Math", 12),), ["Math"]), ((("Math", 10), ("English", 5)), ["Math", "English"]), ((), []))
)
def test_add_subjects(subjects, expected):
    tester = Tester()
    tester.add_subjects(subjects)
    assert list(tester.university.subjects.keys()) == expected


@pytest.mark.parametrize(
    "students,expected",
    (
        ((("Bob", "Bobov", []), ("Ivan", "Ivanov", [])), 2),
        ((("Bob", "Bobov", []), ("Bob", "Bobov", []), ("Ivan", "Ivanov", [])), 3),
        ((("Ivan", "Bobov", []),), 1),
    ),
)
def test_add_students(students, expected):
    tester = Tester()
    tester.add_students(students)
    assert len(tester.university.students.items()) == expected


@pytest.mark.parametrize(
    "professors,expected",
    (
        ((("Bob", "Bobov", []), ("Ivan", "Ivanov", [])), 2),
        ((("Bob", "Bobov", []), ("Bob", "Bobov", []), ("Ivan", "Ivanov", [])), 3),
        ((("Ivan", "Bobov", []),), 1),
    ),
)
def test_add_students(professors, expected):
    tester = Tester()
    tester.add_professor(professors)
    assert len(tester.university.professors.items()) == expected


@pytest.mark.parametrize(
    "name,surname,extra_id,subjects",
    (("Bob", "Bobov", 1, ["Chemistry"]), ("Sim", "DenTron", 0, ["Math"]), ("Boris", "Borisoc", 0, ["Russian"])),
)
def test_sign_student(name, surname, extra_id, subjects):
    tester = Tester()
    tester.add_sub_case()
    tester.add_students_case()
    tester.university.add_student(name, surname, subjects)
    assert Student(name, surname, extra_id) in tester.university.subjects[subjects[0]].grades.keys()


@pytest.mark.parametrize(
    "name,surname,extra_id,subjects",
    (("Kate", "Kane", 1, ["Chemistry"]), ("Sim", "DenTron", 0, ["Math"]), ("Boris", "Borisoc", 0, ["Russian"])),
)
def test_sign_professor(name, surname, extra_id, subjects):
    tester = Tester()
    tester.add_sub_case()
    tester.add_professor_case()
    tester.university.add_professor(name, surname, subjects)
    assert Professor(name, surname, extra_id) in tester.university.subjects[subjects[0]].professors


@pytest.mark.parametrize(
    "name,surname,expected",
    (("Anton", "Antonov", 32), ("Nikita", "Volkov", 44), ("Maksim", "Popov", 0), ("Kate", "Kane", 20)),
)
def test_get_workload(name, surname, expected):
    tester = Tester()
    tester.add_sub_case()
    tester.add_professor_case()
    assert tester.university.get_professors_workload(name, surname) == expected


@pytest.mark.parametrize("subject,expected", (("Math", 2.0), ("English", 3.75), ("Chemistry", 0.0), ("Russian", 5.0)))
def test_get_average_sub(subject, expected):
    tester = Tester()
    tester.add_sub_case()
    tester.add_students_case()
    tester.set_grades_case()
    assert tester.university.get_average_sub(subject) == expected


@pytest.mark.parametrize(
    "name,surname,expected",
    (("Bob", "Bobov", 4.5), ("Andrew", "Tate", 6.0), ("Ivan", "Hope", 0.0), ("Ben", "Benedict", 2.5)),
)
def test_get_average_sub(name, surname, expected):
    tester = Tester()
    tester.add_sub_case()
    tester.add_students_case()
    tester.set_grades_case()
    assert tester.university.get_average_student(name, surname) == expected


@pytest.mark.parametrize(
    "name,surname,subjects", (("Ioan", "Brom", ["Geometry"]), ("Nick", "Bu", ["Chemetry", "History"]))
)
def test_add_student_no_sub(name, surname, subjects):
    tester = Tester()
    tester.add_sub_case()
    tester.add_students_case()
    with pytest.raises(KeyError):
        tester.university.add_student(name, surname, subjects)


@pytest.mark.parametrize(
    "name,surname,subjects", (("Goga", "Boha", ["Biology"]), ("Pupa", "Gupa", ["Chemetry", "History"]))
)
def test_add_professord_no_sub(name, surname, subjects):
    tester = Tester()
    tester.add_sub_case()
    tester.add_professor_case()
    with pytest.raises(KeyError):
        tester.university.add_professor(name, surname, subjects)


@pytest.mark.parametrize(
    "name,surname,extra_id,subject", (("Bob", "Bobov", 0, "Math"), ("Andrew", "Tate", 0, "English"))
)
def test_sign_student_error(name, surname, extra_id, subject):
    tester = Tester()
    tester.add_sub_case()
    tester.add_students_case()
    with pytest.raises(DoubleRegestration):
        tester.university.sign_student(subject, name, surname, extra_id)


@pytest.mark.parametrize("title,week_count", (("English", 13), ("Math", 14), ("Physic", 0)))
def teste_add_subject_error(title, week_count):
    tester = Tester()
    tester.add_sub_case()
    with pytest.raises(DoubleRegestration):
        tester.university.add_subject(title, week_count)


@pytest.mark.parametrize("name,surname,extra_id", (("Bob", "Bobov", 1), ("Andrew", "Jack", 0)))
def test_sign_student_error(name, surname, extra_id):
    tester = Tester()
    tester.add_sub_case()
    tester.add_students_case()
    tester.set_grades_case()
    with pytest.raises(KeyError):
        tester.university.get_average_student(name, surname, extra_id)


@pytest.mark.parametrize("title", (("Geometry",), ("History",), ("PEE",)))
def teste_get_average_sub_error(title):
    tester = Tester()
    tester.add_sub_case()
    with pytest.raises(KeyError):
        tester.university.get_average_sub(title)


@pytest.mark.parametrize("name,surname,extra_id", (("Goga", "Boha", 0), ("Kate", "Kane", 1)))
def test_get_workload_error(name, surname, extra_id):
    tester = Tester()
    tester.add_sub_case()
    tester.add_professor_case()
    with pytest.raises(KeyError):
        tester.university.get_professors_workload(name, surname, extra_id)
