from rest_framework import generics

from university_project.students.models import Student, Course
from .serializers import StudentSerializer, CourseSerializer

class StudentListAPI(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer



class StudentDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer    

class CourseListAPI(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer    