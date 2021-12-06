from django.contrib import admin

# Register your models here.
from .models import Student, Tutor, Course, Enrollment, Task


admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Task)