from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentListView,
    CourseListView,
    StudentCreateView,
    CourseCreateView,
    StudentUpdateView,
    StudentDeleteView,
)
from .api_views import (
    StudentViewSet,
    CourseViewSet,
    ProfessorViewSet,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="student")
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"professors", ProfessorViewSet, basename="professor")
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("api/v1/", include(router.urls)),  # API versioning: v1
    path("students/", StudentListView.as_view(), name="student_list"),
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("students/create/", StudentCreateView.as_view(), name="create_student"),
    path("courses/create/", CourseCreateView.as_view(), name="create_course"),
    path("students/<int:pk>/edit/", StudentUpdateView.as_view(), name="edit_student"),
    path(
        "students/<int:pk>/delete/", StudentDeleteView.as_view(), name="delete_student"
    ),
]
