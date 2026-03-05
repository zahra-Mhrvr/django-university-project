from django.urls import path
from .views import (
    StudentListView,
    CourseListView,
    StudentCreateView,
    CourseCreateView,
    StudentUpdateView,
    StudentDeleteView,
)
from .api_views import (
    StudentListAPI,
    StudentDetailAPI,
    CourseListAPI,
    CourseDetailAPI
)

urlpatterns = [
    path('students/', StudentListView.as_view(), name='student_list'),
    path('courses/', CourseListView.as_view(), name='course_list'),

    path('students/create/', StudentCreateView.as_view(), name='create_student'),
    path('courses/create/', CourseCreateView.as_view(), name='create_course'),

    path('students/<int:pk>/edit/', StudentUpdateView.as_view(), name='edit_student'),
    path('students/<int:pk>/delete/', StudentDeleteView.as_view(), name='delete_student'),
]

urlpatterns += [

    path('api/students/', StudentListAPI.as_view(), name='api_students'),

    path('api/students/<int:pk>/', StudentDetailAPI.as_view(), name='api_student_detail'),

    path('api/courses/', CourseListAPI.as_view(), name='api_courses'),

    path('api/courses/<int:pk>/', CourseDetailAPI.as_view(), name='api_course_detail'),

]