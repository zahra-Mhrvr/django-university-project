import pytest

from students.forms import StudentForm, CourseForm, StudentAdminForm, CourseAdminForm
from students.models import Student, Course, Category, Professor


# ---------------------- Fixtures ----------------------
@pytest.fixture
def category():
    return Category.objects.create(name="Computer Science")


@pytest.fixture
def professor():
    return Professor.objects.create(
        first_name="Alan", last_name="Turing", email="alan@uni.com"
    )


@pytest.fixture
def course(category, professor):
    return Course.objects.create(
        name="Algorithms", code="CS101", category=category, professor=professor
    )


# ---------------------- StudentForm Tests ----------------------
@pytest.mark.django_db
def test_student_form_valid(course):
    form_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "student_id": "STU001",
        "courses": [course.id],
    }
    form = StudentForm(data=form_data)
    assert form.is_valid()


# ---------------------- CourseForm Tests ----------------------
@pytest.mark.django_db
def test_course_form_valid(category, professor):
    form_data = {
        "name": "Algorithms",
        "code": "CS101",
        "category": category.id,
        "professor": professor.id,
    }
    form = CourseForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_course_form_missing_category(professor):
    # category missing
    form_data = {
        "name": "Algorithms",
        "code": "CS101",
        "professor": professor.id,
    }
    form = CourseForm(data=form_data)
    assert not form.is_valid()
    assert "category" in form.errors


# ---------------------- StudentAdminForm Tests ----------------------
@pytest.mark.django_db
@pytest.mark.parametrize(
    "existing_data,new_data,should_be_valid,error_msg",
    [
        # No duplicate exists
        (
            None,
            {"first_name": "Bob", "last_name": "Marley", "student_id": "STU999"},
            True,
            None,
        ),
        # Duplicate first+last name
        (
            {"first_name": "Alice", "last_name": "Smith", "student_id": "STU001"},
            {"first_name": "Alice", "last_name": "Smith", "student_id": "STU002"},
            False,
            "already exists",
        ),
    ],
)
def test_student_admin_form(
    existing_data, new_data, should_be_valid, error_msg, course
):
    # Create existing student if needed
    if existing_data:
        Student.objects.create(**existing_data)

    # Add required courses field
    new_data["courses"] = [course.id]

    form = StudentAdminForm(data=new_data)
    if should_be_valid:
        assert form.is_valid()
    else:
        assert not form.is_valid()
        assert error_msg in str(form.errors)


# ---------------------- CourseAdminForm Tests ----------------------
@pytest.mark.django_db
@pytest.mark.parametrize(
    "existing_data,new_data,should_be_valid,error_msg",
    [
        # No duplicate
        (None, {"name": "Databases", "code": "CS201"}, True, None),
        # Duplicate course name
        (
            {
                "name": "Algorithms",
                "code": "CS101",
                "category_name": "CS",
                "professor_name": "Alan Turing",
            },
            {"name": "Algorithms", "code": "CS999"},
            False,
            "already exists",
        ),
    ],
)
def test_course_admin_form(
    existing_data, new_data, should_be_valid, error_msg, category, professor
):
    # Create existing course if needed
    if existing_data:
        Course.objects.create(
            name=existing_data["name"],
            code=existing_data["code"],
            category=category,
            professor=professor,
        )

    # Add required category and professor if missing
    new_data.setdefault("category", category.id)
    new_data.setdefault("professor", professor.id)

    form = CourseAdminForm(data=new_data)
    if should_be_valid:
        assert form.is_valid()
    else:
        assert not form.is_valid()
        assert error_msg in str(form.errors)
