from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Student, Course, Professor, Category
from .serializers import (
    StudentSerializer,
    CourseSerializer,
    ProfessorSerializer,
    CategorySerializer,
)


class StudentViewSet(viewsets.ModelViewSet):

    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]

    search_fields = ["first_name", "last_name", "student_id"]

    ordering_fields = ["first_name", "last_name", "student_id"]

    filterset_fields = ["student_id"]


class CourseViewSet(viewsets.ModelViewSet):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ["name", "code"]

    ordering_fields = ["name", "code"]


class ProfessorViewSet(viewsets.ModelViewSet):

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ["first_name", "last_name"]

    ordering_fields = ["first_name", "last_name"]


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ["name"]

    ordering_fields = ["name"]
