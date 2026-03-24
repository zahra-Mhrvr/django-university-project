import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User

from students.models import Student, Course, Professor, Category

@pytest.fixture
def user(db):
    return User.objects.create_user(username="apiuser", password="pass123")


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.login(username="apiuser", password="pass123")
    return client


@pytest.mark.django_db
def test_api_requires_authentication():

    client = APIClient()

    url = reverse('student-list')  # DRF auto-name

    response = client.get(url)

    assert response.status_code == 403



@pytest.mark.django_db
def test_get_students(api_client):

    Student.objects.create(first_name="Alice", last_name="Smith", student_id="1")

    url = reverse('student-list')

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data["results"]) == 1



@pytest.mark.django_db
def test_create_student(api_client):

    url = reverse('student-list')

    data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "student_id": "STU123"
    }

    response = api_client.post(url, data)

    assert response.status_code == 201
    assert Student.objects.count() == 1



@pytest.mark.django_db
def test_student_search(api_client):

    Student.objects.create(first_name="Alice", last_name="Smith", student_id="1")
    Student.objects.create(first_name="Bob", last_name="Brown", student_id="2")

    url = reverse('student-list')

    response = api_client.get(url + "?search=Alice")

    assert response.status_code == 200
    assert len(response.data["results"]) == 1



@pytest.mark.django_db
def test_student_filter(api_client):

    Student.objects.create(first_name="Alice", last_name="Smith", student_id="A1")
    Student.objects.create(first_name="Bob", last_name="Brown", student_id="B1")

    url = reverse('student-list')

    response = api_client.get(url + "?student_id=A1")

    assert response.status_code == 200
    assert len(response.data["results"]) == 1



@pytest.mark.django_db
def test_student_ordering(api_client):

    Student.objects.create(first_name="Charlie", last_name="Z", student_id="3")
    Student.objects.create(first_name="Alice", last_name="A", student_id="1")

    url = reverse('student-list')

    response = api_client.get(url + "?ordering=first_name")

    assert response.status_code == 200

    results = response.data["results"]

    names = [student["first_name"] for student in results]

    assert names == sorted(names)



@pytest.mark.django_db
def test_update_student_api(api_client):

    student = Student.objects.create(
        first_name="Old",
        last_name="Name",
        student_id="STU1"
    )

    url = reverse('student-detail', args=[student.id])

    response = api_client.patch(url, {
        "first_name": "New"
    })

    student.refresh_from_db()

    assert response.status_code == 200
    assert student.first_name == "New"


@pytest.mark.django_db
def test_delete_student_api(api_client):

    student = Student.objects.create(
        first_name="Delete",
        last_name="Me",
        student_id="STU9"
    )

    url = reverse('student-detail', args=[student.id])

    response = api_client.delete(url)

    assert response.status_code == 204
    assert Student.objects.count() == 0