import pytest
from students.models import Student, Course, Professor, Category


@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(name="Computer Science")

    assert category.name == "Computer Science"
    assert Category.objects.count() == 1


@pytest.mark.django_db
def test_professor_creation():
    professor = Professor.objects.create(
        first_name="Alan", last_name="Turing", email="alan@university.com"
    )

    assert professor.first_name == "Alan"
    assert professor.email == "alan@university.com"
    assert Professor.objects.count() == 1


@pytest.mark.django_db
def test_course_creation():

    category = Category.objects.create(name="Mathematics")

    professor = Professor.objects.create(
        first_name="Ada", last_name="Lovelace", email="ada@university.com"
    )

    course = Course.objects.create(
        name="Algorithms", code="CS101", category=category, professor=professor
    )

    assert course.name == "Algorithms"
    assert course.code == "CS101"


@pytest.mark.django_db
def test_student_creation():

    student = Student.objects.create(
        first_name="John", last_name="Doe", student_id="STU001"
    )

    assert student.first_name == "John"
    assert student.student_id == "STU001"


@pytest.mark.django_db
def test_student_course_enrollment():

    category = Category.objects.create(name="Engineering")

    professor = Professor.objects.create(
        first_name="Grace", last_name="Hopper", email="grace@university.com"
    )

    course = Course.objects.create(
        name="Compilers", code="CS404", category=category, professor=professor
    )

    student = Student.objects.create(
        first_name="Alice", last_name="Smith", student_id="STU100"
    )

    student.courses.add(course)

    assert student.courses.count() == 1
    assert student.courses.first().name == "Compilers"


@pytest.mark.django_db
def test_student_ordering():

    Student.objects.create(first_name="Alice", last_name="Smith", student_id="1")

    Student.objects.create(first_name="Bob", last_name="Brown", student_id="2")

    Student.objects.create(first_name="Charlie", last_name="Adams", student_id="3")

    students = list(Student.objects.all())

    assert students[0].last_name == "Adams"
    assert students[1].last_name == "Brown"
    assert students[2].last_name == "Smith"
