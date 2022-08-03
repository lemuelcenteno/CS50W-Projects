from django.urls import path


from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("", views.CourseListView.as_view(), name="index"),
    path("register/", views.SignUpView.as_view(), name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="school/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("home/", views.User_CourseListView.as_view(), name="user-index"),
    path("search/", views.Search_CourseListView.as_view(), name="search"),
    path("courses/add/", views.CourseAddView.as_view(), name="course-add"),
    path("course/<str:code>/", views.CourseDetailView.as_view(), name="course-detail"),
    path(
        "course/<str:code>/student-api/",
        views.course_student_api,
        name="course-student-api",
    ),
    path(
        "course/<str:code>/teacher-api/",
        views.course_teacher_api,
        name="course-teacher-api",
    ),
    path("course/<str:code>/delete/", views.course_delete, name="course-delete"),
]
