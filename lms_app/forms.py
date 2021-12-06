from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Tutor, Course, Task


class DateInput(forms.DateInput):
    input_type = 'date'


class UserForm(forms.ModelForm):
    is_staff = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('email', 'department', 'group_number', 'photo',)


class MentorForm(forms.ModelForm):

    class Meta:
        model = Tutor
        fields = ('email', 'position', 'photo',)


class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'description')


class DepartmentsChoiceForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('department',)


class TaskCreationForm(forms.ModelForm):
    course = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Task
        fields = ('title', 'type', 'content', 'deadline', 'max_grade')
        widgets = {
            'deadline': DateInput(),
        }