from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Tutor, Course, Task, TaskFile, TestPackage, TestQuestion


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

    class Meta:
        model = Task
        fields = ('title', 'content', 'deadline', 'max_grade')
        widgets = {
            'deadline': DateInput(),
        }

class TestTaskCreationForm(forms.ModelForm):
    course = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    test_package = forms.ModelMultipleChoiceField(queryset=TestPackage.objects.all())

    class Meta:
        model = Task
        fields = ('title', 'content', 'deadline', 'max_grade')
        widgets = {
            'deadline': DateInput(),
        }


class TaskFileForm(forms.ModelForm):
    class Meta:
        model = TaskFile
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False


class TaskTypeChoiceForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('type',)

class TestPackageCreationForm(forms.Form):

    test_package_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id')
        questions = kwargs.pop('questions')
        answer_choices = kwargs.pop('answer_choices')
        answer_choices = [(str(x),str(x)) for x in answer_choices]
        super(TestPackageCreationForm, self).__init__(*args, **kwargs)
        counter = 1
        self.fields['course_id'] = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=course_id)
        for q in questions:
            self.fields['question-' + str(counter)] = forms.CharField(label=f"Question {str(counter)}",
                                                                      initial=q)
            for ans in answer_choices:
                self.fields['question-answer' + str(counter) + str(ans[0])] = \
                    forms.CharField(label=f"Answer variant {str(ans[0])} for question {str(counter)}")
            self.fields['question-correct-answer' + str(counter)] = \
                forms.ChoiceField(choices=answer_choices,
                                  widget=forms.RadioSelect,
                                  label=f"Correct answer for question {str(counter)}")
            counter += 1

class TestTaskInfoForm(forms.Form):
    questions_amount = forms.IntegerField(label="Questions amount (Text is typed manually)")
    questions_list = forms.CharField(label="Questions list (Optional)")
    answer_variants_amount = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(TestTaskInfoForm, self).__init__(*args, **kwargs)
        self.fields['questions_list'].required = False
