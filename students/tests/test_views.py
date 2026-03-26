import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User, Permission

from students.models import Student, Course, Category, Professor

# =========================
# Fixtures
# =========================


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="pass123")


@pytest.fixture
def client_logged_in(user):
    client = Client()
    client.login(username="testuser", password="pass123")
    return client


@pytest.fixture
def user_with_permissions(db):
    user = User.objects.create_user(username="admin", password="pass123")

    permissions = Permission.objects.filter(
        codename__in=["add_student", "change_student", "delete_student"]
    )
    user.user_permissions.set(permissions)

    return user


@pytest.fixture
def client_with_permissions(user_with_permissions):
    client = Client()
    client.login(username="admin", password="pass123")
    return client


@pytest.fixture
def course_setup(db):
    category = Category.objects.create(name="Engineering")

    professor = Professor.objects.create(
        first_name="Alan", last_name="Turing", email="alan@uni.com"
    )

    course = Course.objects.create(
        name="Algorithms", code="CS101", category=category, professor=professor
    )

    return course


# =========================
# Student List View
# =========================


@pytest.mark.django_db
def test_student_list_view_logged_in(client_logged_in):
    url = reverse("student_list")
    response = client_logged_in.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_student_list_requires_login():
    client = Client()
    url = reverse("student_list")

    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_student_list_count(client_logged_in):

    Student.objects.create(first_name="Alice", last_name="Smith", student_id="STU1")
    Student.objects.create(first_name="Bob", last_name="Brown", student_id="STU2")
    Student.objects.create(first_name="Charlie", last_name="Davis", student_id="STU3")

    url = reverse("student_list")
    response = client_logged_in.get(url)

    page_obj = response.context["page_obj"]

    assert page_obj.paginator.count == 3


# =========================
# Create Student
# =========================


@pytest.mark.django_db
def test_create_student(client_with_permissions, course_setup):

    url = reverse("create_student")

    response = client_with_permissions.post(
        url,
        {
            "first_name": "Alice",
            "last_name": "Smith",
            "student_id": "STU123",
            "courses": [course_setup.id],  # ✅ REQUIRED
        },
    )

    assert response.status_code == 302
    assert Student.objects.count() == 1


@pytest.mark.django_db
def test_create_student_without_permission(client_logged_in, course_setup):

    url = reverse("create_student")

    response = client_logged_in.post(
        url,
        {
            "first_name": "Bob",
            "last_name": "Brown",
            "student_id": "STU999",
            "courses": [course_setup.id],
        },
    )

    assert response.status_code == 403


# =========================
# Update Student
# =========================


@pytest.mark.django_db
def test_update_student(client_with_permissions, course_setup):

    student = Student.objects.create(
        first_name="Old", last_name="Name", student_id="STU001"
    )

    student.courses.add(course_setup)

    url = reverse("edit_student", args=[student.id])

    response = client_with_permissions.post(
        url,
        {
            "first_name": "New",
            "last_name": "Name",
            "student_id": "STU001",
            "courses": [course_setup.id],
        },
    )

    student.refresh_from_db()

    assert response.status_code == 302
    assert student.first_name == "New"


# =========================
# Delete Student
# =========================


@pytest.mark.django_db
def test_delete_student(client_with_permissions):

    student = Student.objects.create(
        first_name="Delete", last_name="Me", student_id="STU777"
    )

    url = reverse("delete_student", args=[student.id])

    response = client_with_permissions.post(url)

    assert response.status_code == 302
    assert Student.objects.count() == 0


# =========================
# Course List View
# =========================


@pytest.mark.django_db
def test_course_list_view(client_logged_in):

    url = reverse("course_list")
    response = client_logged_in.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_student_search(client_logged_in):

    Student.objects.create(first_name="Alice", last_name="Smith", student_id="1")
    Student.objects.create(first_name="Bob", last_name="Brown", student_id="2")

    url = reverse("student_list")

    response = client_logged_in.get(url + "?q=Alice")

    students = response.context["students"]

    assert len(students) == 1
    assert students[0].first_name == "Alice"


@pytest.mark.django_db
def test_filter_by_course(client_logged_in):

    category = Category.objects.create(name="Engineering")

    professor = Professor.objects.create(
        first_name="Alan", last_name="Turing", email="alan@uni.com"
    )

    course = Course.objects.create(
        name="Algorithms", code="CS101", category=category, professor=professor
    )

    student = Student.objects.create(
        first_name="Alice", last_name="Smith", student_id="1"
    )

    student.courses.add(course)

    url = reverse("student_list")

    response = client_logged_in.get(url + f"?course={course.id}")

    students = response.context["students"]

    assert len(students) == 1


@pytest.mark.django_db
def test_filter_by_category(client_logged_in):

    category = Category.objects.create(name="Engineering")

    professor = Professor.objects.create(
        first_name="Alan", last_name="Turing", email="alan@uni.com"
    )

    course = Course.objects.create(
        name="Algorithms", code="CS101", category=category, professor=professor
    )

    student = Student.objects.create(
        first_name="Alice", last_name="Smith", student_id="1"
    )

    student.courses.add(course)

    url = reverse("student_list")

    response = client_logged_in.get(url + "?category=Engineering")

    students = response.context["students"]

    assert len(students) == 1
