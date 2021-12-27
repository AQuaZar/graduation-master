from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image
from .nlp import get_sentences
import os

DEPARTMENT_CHOICES = [
    ('feba', 'FEBA'),
    ('fmv', 'FMV'),
    ('fabd', 'FABD'),
    ('faet', 'FAET'),
    ('uf', 'UF'),
    ('akf', 'AKF'),
    ('fccpi', 'FCCPI'),
    ('ftml', 'FTML'),
    ('flsk', 'FLSK'),
]

TASK_CHOICES = [
    ('TEST', 'New Test Package'),
    ('XTEST', 'Existing Test'),
    ('BASE', 'Basic'),
]

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='students')
    department = models.CharField(max_length=5, choices=DEPARTMENT_CHOICES)
    group_number = models.CharField(
        max_length=3, validators=[RegexValidator(r"^\d{1,10}$")]
    )
    email = models.EmailField()
    course_enrollments = models.ManyToManyField('Course', through='Enrollment')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        super().save()
        if self.photo:
            try:
                img = Image.open(self.photo.path)
            except FileNotFoundError:
                img = Image.open(os.path.abspath("lms_app/anon.jpeg"))
            width, height = img.size  # Get dimensions

            if width > 300 and height > 300:
                # keep ratio but shrink down
                img.thumbnail((width, height))

            # check which one is smaller
            if height < width:
                # make square by cutting off equal amounts left and right
                left = (width - height) / 2
                right = (width + height) / 2
                top = 0
                bottom = height
                img = img.crop((left, top, right, bottom))

            elif width < height:
                # make square by cutting off bottom
                left = 0
                right = width
                top = 0
                bottom = width
                img = img.crop((left, top, right, bottom))

            if width > 300 and height > 300:
                img.thumbnail((300, 300))

            img.save(self.photo.path)


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='tutors')
    position = models.CharField(max_length=75, default='')
    email = models.EmailField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        super().save()
        if self.photo:
            try:
                img = Image.open(self.photo.path)
            except FileNotFoundError:
                img = Image.open(os.path.abspath("lms_app/anon.jpeg"))
            width, height = img.size  # Get dimensions

            if width > 300 and height > 300:
                # keep ratio but shrink down
                img.thumbnail((width, height))

            # check which one is smaller
            if height < width:
                # make square by cutting off equal amounts left and right
                left = (width - height) / 2
                right = (width + height) / 2
                top = 0
                bottom = height
                img = img.crop((left, top, right, bottom))

            elif width < height:
                # make square by cutting off bottom
                left = 0
                right = width
                top = 0
                bottom = width
                img = img.crop((left, top, right, bottom))

            if width > 300 and height > 300:
                img.thumbnail((300, 300))

            img.save(self.photo.path)

@receiver(post_save, sender=User)
def create_user_role(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            Tutor.objects.create(user=instance)
        else:
            Student.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_role(sender, instance, **kwargs):
    try:
        if instance.is_staff:
            instance.tutor.save()
        else:
            instance.student.save()
    except ObjectDoesNotExist:
        Tutor.objects.create(user=instance)

class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    created_by = models.ForeignKey(Tutor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class TestPackage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(Tutor, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Task(models.Model):
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TASK_CHOICES)
    content = models.TextField(default='')
    start_date = models.DateTimeField(auto_now_add=True, editable=False)
    deadline = models.DateTimeField()
    max_grade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    test_package = models.ForeignKey(TestPackage, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title}"


class TaskFile(models.Model):
    file = models.FileField(upload_to="task_docs")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class TestQuestion(models.Model):
    test_package = models.ForeignKey(TestPackage, on_delete=models.CASCADE)
    question = models.CharField(max_length=400)
    answer_variants = models.CharField(max_length=400)
    answer = models.CharField(max_length=100)


    @property
    def variants_list(self):
        return get_sentences(self.answer_variants)

    def is_correct_answer(self, user_answer):
        return user_answer.strip().lower() == self.answer.strip().lower()


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    start_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.student.user.last_name} {self.student.user.first_name} " \
               f"{self.student.department} {self.student.group_number} {self.course.name}"

class Invites(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)





