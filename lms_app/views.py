from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from lms_app.forms import UserForm, StudentForm, MentorForm, CourseCreationForm, DepartmentsChoiceForm, TaskCreationForm
from django.db import transaction
from .models import Course, Tutor, Student, User, Enrollment, Invites, Task
from django.http import HttpResponseNotFound
from django.contrib import messages
# Create your views here.


def home_view(request):
    data = {}
    if request.user.is_authenticated and not request.user.is_staff:
        invites = Invites.objects.filter(student=request.user.student.id)
        if invites:
            data["invites"] = invites

    return render(request, "home.html", context=data)


@transaction.atomic
def create_user_view(request, role:str):
    if request.method == 'POST':

        if role == 'student':
            user_form = UserForm(request.POST, initial={'is_staff': False})
            #user_form.cleaned_data['is_staff'] = False
            profile_form = StudentForm(request.POST, files=request.FILES)
        elif role == 'mentor':
            user_form = UserForm(request.POST, initial={'is_staff': True})
            profile_form = MentorForm(request.POST, files=request.FILES)
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.email = profile_form.cleaned_data['email']
            if role == 'mentor':
                user_form.cleaned_data['is_staff'] = True
            user.is_staff = user_form.cleaned_data['is_staff']
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            user.refresh_from_db()  # This will load the Profile created by the Signal
            if role == 'student':
                profile_form = StudentForm(request.POST, files=request.FILES, instance=user.student)  # Reload the profile form with the profile instance
            elif role == 'mentor':
                profile_form = MentorForm(request.POST, files=request.FILES, instance=user.tutor)
            profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
            profile_form.save()  # Gracefully save the form
            # Authenticate user and redirect
            user = authenticate(request,
                                username=user_form.cleaned_data['username'],
                                password=user_form.cleaned_data['password'])
            print(user)
            if user is not None:
                login(request, user)
                return redirect(resolve_url('home'))
    else:
        user_form = UserForm()
        if role == 'student':
            profile_form = StudentForm()
        elif role == 'mentor':
            profile_form = MentorForm()
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, 'registration/sign_up.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'role': role.capitalize()
    })


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard_view(request):
    courses = []
    if request.user.is_authenticated and request.user.is_staff:
        courses = list(Course.objects.filter(created_by=request.user.tutor.id))
    elif request.user.is_authenticated:
        enrollments = Enrollment.objects.filter(student=request.user.student)
        for enrollment in enrollments:
            courses.append(enrollment.course)
    return render(request, 'dashboard.html', context={"courses":courses})

@login_required
def course_creation_view(request):
    if request.method=="GET":
        course_creation_form = CourseCreationForm()
        return render(request, 'course_creation.html', context={"form":course_creation_form})
    else:
        course_creation_form = CourseCreationForm(request.POST)
        if course_creation_form.is_valid():
            new_course = course_creation_form.save(commit=False)
            new_course.created_by = request.user.tutor
            course_creation_form.save()
            return redirect(resolve_url('dashboard'))

@login_required
def course_page_view(request, username, id):
    tutor = User.objects.get(username=username)
    enrolled_students = []
    department_students = []
    course = None
    dep_form = None
    tasks = []

    if tutor:
        course = Course.objects.get(created_by=tutor.tutor, id=id)
        if course:
            for enrollment in Enrollment.objects.filter(course_id=id):
                enrolled_students.append(enrollment.student)

            tasks = Task.objects.filter(course=course)

            dep_form = DepartmentsChoiceForm()
            if request.method=="POST":
                department = request.POST.get('department')
                if department:
                    for department_student in Student.objects.filter(department=department):
                        if department_student not in enrolled_students:
                            department_students.append(department_student)
                invite_count = 0
                for post_object in request.POST:
                    if 'invite' in post_object:
                        student_id = request.POST[post_object]
                        student = Student.objects.get(id=int(student_id))
                        invite = Invites(course=course, student=student)
                        invite.save()
                        invite_count += 1
                if invite_count > 0:
                    messages.success(request, f'Invites to {invite_count} students were successfully sent.')

    data = {"toEdit": False, "course": course, "students": enrolled_students,
            "dep_form": dep_form, "dep_students": department_students, "tasks": tasks}
    return render(request, 'course_page.html', context=data)

@require_http_methods(["POST"])
def process_invite(request):
    print(request.POST)
    for key, value in request.POST.items():
        if key == "accept":
            invite = Invites.objects.get(id=value)
            if invite:
                enrollment = Enrollment(course=invite.course, student=invite.student)
                enrollment.save()
                invite.delete()
        elif key == "decline":
            invite = Invites.objects.get(id=value)
            if invite:
                invite.delete()
    return redirect(resolve_url('home'))


@login_required()
def create_task(request, course_id):
    if request.method=="GET":
        task_creation_form = TaskCreationForm()
        return render(request, 'course_creation.html', context={"form":task_creation_form})
    else:
        course = Course.objects.get(id=course_id)
        task_creation_form = TaskCreationForm(request.POST, files=request.FILES, initial={"course":course})
        if task_creation_form.is_valid():
            task = task_creation_form.save(commit=False)
            task.course = course
            task.save()
        return redirect(resolve_url('dashboard'))

        # if course_creation_form.is_valid():
        #     # new_course = course_creation_form.save(commit=False)
        #     # new_course.created_by = request.user.tutor
        #     # course_creation_form.save()
        #     return redirect(resolve_url('dashboard'))
    return render(request, 'task_creation_page.html')


@login_required()
def profile_page_view(request):
    return render(request, 'profile_page.html')