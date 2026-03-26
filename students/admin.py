from django.contrib import admin
from .models import Student, Course
from .forms import StudentAdminForm, CourseAdminForm


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    list_display = ("student_id", "first_name", "last_name")
    search_fields = ("first_name", "last_name", "student_id")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ("code", "name", "category")
    search_fields = ("name", "code")
