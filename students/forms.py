from django import forms
from .models import Student, Course
from django.core.exceptions import ValidationError
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_id', 'courses']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code','category', 'professor']
 
class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        student_id = cleaned_data.get("student_id")

        if first_name and last_name:
            existing = Student.objects.filter(
                first_name__iexact=first_name,
                last_name__iexact=last_name
            ).exclude(student_id=student_id)
            
            if existing.exists():
                # Raise a warning instead of blocking
                raise ValidationError(
                    f"A student named {first_name} {last_name} already exists "
                    f"with a different Student ID. Are you sure you want to add this?"
                )

        return cleaned_data
    

    # students/forms.py
class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        code = cleaned_data.get("code")

        if name:
            existing = Course.objects.filter(name__iexact=name).exclude(code=code)
            if existing.exists():
                raise ValidationError(
                    f"A course named '{name}' already exists with a different code. "
                    f"Are you sure you want to add this?"
                )
        return cleaned_data