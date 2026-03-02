from django.db import models
from django.db.models.functions import Lower

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Professor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    professor = models.ForeignKey('Professor', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=20, unique=True)
    courses = models.ManyToManyField(Course, related_name="students")
    
    class Meta:
            ordering = [Lower('last_name'), Lower('first_name')]
    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"

