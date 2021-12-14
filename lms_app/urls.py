from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('sign_up/<str:role>', views.create_user_view, name='signup'),
    path('logout/', views.logout_view, name='logout-custom'),
    path('create_course', views.course_creation_view, name='create_course'),
    path('courses/<str:username>/<int:id>', views.course_page_view, name='course_page'),
    path('accounts/profile/', views.profile_page_view, name='profile'),
    path('process-invite/', views.process_invite, name='process-invite'),
    path('create-task/<int:course_id>', views.create_task, name='create-task'),
    path('courses/<str:username>/<int:course_id>/<int:task_id>/', views.task_page_view, name='task-page'),
    path('create-test-package/', views.create_test_package, name='create-test-package')
]