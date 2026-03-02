from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Student, Course, Professor, Category
from .forms import StudentForm, CourseForm
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 10
    

    def get_queryset(self):
        queryset = (
            Student.objects
            .prefetch_related('courses')
            .order_by('last_name', 'first_name', 'id')
        )

        search_query = self.request.GET.get('q')
        course_filter = self.request.GET.get('course')
        category_filter = self.request.GET.get('category')

        # Search by student name
        if search_query:
            queryset = queryset.filter(
                first_name__icontains=search_query
            ) | queryset.filter(
                last_name__icontains=search_query
            )

        # Filter by specific course
        if course_filter:
            queryset = queryset.filter(courses__id=course_filter)

        # Filter by category (IMPORTANT FIX HERE)
        if category_filter:
            queryset = queryset.filter(
                courses__category__name__iexact=category_filter
            )

        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['categories'] = Category.objects.all()
        return context
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        queryset = Course.objects.select_related('professor')

        category_filter = self.request.GET.get('category')

        if category_filter:
            queryset = queryset.filter(category__icontains=category_filter)

        return queryset.distinct()
class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/create_student.html'
    success_url = reverse_lazy('student_list')

    permission_required = 'students.add_student'
class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'students/create_course.html'
    success_url = reverse_lazy('course_list')

    permission_required = 'students.add_course'
class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    permission_required = 'students.change_student'
class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')

    permission_required = 'students.delete_student'
