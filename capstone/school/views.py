import json

from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login


from .forms import *


# Class-based views
class SignUpView(SuccessMessageMixin, CreateView):
    """
    For user registration, either as a teacher/student.
    """
    template_name = "school/register.html"
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully."

    # If registration successful, login and redirect to home (user-index)
    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("user-index")


class CourseAddView(
    SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView
):
    """
    For adding courses.
    CONSTRAINT: Only for teachers.
    """
    template_name = "school/course_add.html"
    success_url = reverse_lazy("user-index")
    form_class = CourseAddForm
    success_message = "Course added successfully."

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.role == "TEA"


class CourseDetailView(LoginRequiredMixin, DetailView):
    """
    For viewing a course in detail.
    ADDITIONALLY:
    STUDENT - can see their grade if enrolled.
    TEACHER - see graded and ungraded students if they manage the course.
    """
    model = Course
    template_name = "school/course_detail.html"
    context_object_name = "course"

    def get_object(self):
        code = self.kwargs["code"]
        try:
            course = Course.objects.get(code=code)
        except Course.DoesNotExist:
            raise Http404(f"No course found with code '{code}'.")
        return course

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            code = self.kwargs["code"]
            try:
                course = Course.objects.get(code=code)
            except Course.DoesNotExist:
                raise Http404(f"No course found with code '{code}'.")
            else:
                # If teacher get gradebooks
                if self.request.user.role == "TEA":
                    gradebooks = sorted(
                        course.gradebooks.all(), key=lambda x: x.student.username
                    )
                    graded = []
                    ungraded = []
                    for gradebook in gradebooks:
                        if gradebook.grade is not None:
                            graded.append(gradebook)
                        else:
                            ungraded.append(gradebook)
                    context["graded"] = graded
                    context["ungraded"] = ungraded
                # If enrolled student, get grade
                else:
                    if user in course.students.all():
                        context["grade"] = Gradebook.objects.get(
                            course=course, student=user
                        ).grade
        return context


class CourseListView(ListView):
    """
    Lists all available courses.
    """
    model = Course
    template_name = "school/course_list_base.html"
    context_object_name = "courses"
    paginate_by = 7

    def get_queryset(self, **kwargs):
        return Course.objects.all().order_by('-timestamp')


class User_CourseListView(LoginRequiredMixin, ListView):
    """
    Lists courses for a student/teacher.
    STUDENT - sees courses they are enrolled in.
    TEACHER - sees courses they manage.
    """
    model = Course
    template_name = "school/course_list_user.html"
    context_object_name = "courses"
    paginate_by = 7

    def get_queryset(self, **kwargs):
        user = self.request.user
        if user.role == "STU":
            queryset = user.attending.all().order_by('-timestamp')
        else:
            queryset = user.teaching.all().order_by('-timestamp')
        return queryset


class Search_CourseListView(ListView):
    """
    Lists courses that match a search query.
    """
    model = Course
    template_name = "school/course_list_search.html"
    context_object_name = "courses"
    order_by = "-timestamp"
    paginate_by = 7

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get courses that match the query 'q'
        context["q"] = self.request.GET["q"].strip()
        q = context["q"].lower()
        return context

    def get_queryset(self, **kwargs):
        # Get courses that match the query 'q'
        q = self.request.GET["q"].strip().lower()
        courses = []
        for course in Course.objects.all().order_by('-timestamp'):
            if course not in courses:
                if q in course.code.lower() or q in course.title.lower():
                    courses.append(course)
        return courses


# decorator for course_student_api
def is_student(user):
    """
    checks if user is a student
    """
    return user.role == "STU"

# Function-based Views
@user_passes_test(is_student)
def course_student_api(request, code):
    """
    For enrolling/unenrolling of students to a course.
    If students is enrolled, get request also returns the student's grade.
    """
    try:
        course = Course.objects.get(code=code)
    except:
        return JsonResponse({"error": "Course not found."}, status=404)
    else:

        user = request.user

        if request.method == "GET":
            # Returns course CODE, TITLE, and STUDENT_COUNT, & student user's ENROLLED (enrollment status)
            # If enrolled: also returns student user's GRADE
            response = {
                "code": course.code,
                "title": course.title,
                "student_count": course.students.all().count(),
                "enrolled": request.user in course.students.all(),
            }
            if response["enrolled"]:
                try:
                    gradebook = Gradebook.objects.get(course=course, student=user)
                except Gradebook.DoesNotExist:
                    return JsonResponse({"error": "Gradebook not found."}, status=404)
                else:
                    response["grade"] = gradebook.grade
            return JsonResponse(response)

        elif request.method == "PUT":
            # PUT requests update student user's enrollment status
            # and ADDS or REMOVES them from the course
            data = json.loads(request.body)
            if data.get("enroll") is not None:
                if data["enroll"] and user not in course.students.all():
                    course.students.add(user)
                    # Create gradebook for student if it doesn't exist yet.
                    try:
                        Gradebook.objects.get(course=course, student=user)
                    except Gradebook.DoesNotExist:
                        gradebook = Gradebook(student=user, course=course)
                        gradebook.save()
                if not data["enroll"] and user in course.students.all():
                    course.students.remove(user)
                    # Delete students gradebook if it exists.
                    try:
                        user_gradebook = Gradebook.objects.get(
                            course=course, student=user
                        )
                    except Gradebook.DoesNotExist:
                        pass
                    else:
                        user_gradebook.delete()
                course.save()
                return JsonResponse(
                    {"success_message": "Operation successful."}, status=200
                )

            else:
                return JsonResponse({"error": "Operation failed."}, status=400)

        # Request for following profile must be PUT or GET
        else:
            return JsonResponse({"error": "GET or PUT request required."}, status=400)


# decorator for teacher_api
def is_teacher(user):
    """
    checks if user is a teacher
    """
    return user.role == "TEA"

@user_passes_test(is_teacher)
def course_teacher_api(request, code):
    """
    For posting and editing student grades.
    CONSTRAINT: Only the teacher who manages a certain course can post/edit grades for that course.
    """
    try:
        course = Course.objects.get(code=code)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    else:
        # Allow changes only if the user is the teacher of the course
        if request.user == course.teacher:

            # For saving/changing grades
            if request.method == "POST":
                for item in request.POST:
                    if item.startswith("gradebook_"):
                        id = int(item.removeprefix("gradebook_"))
                        try:
                            gradebook = Gradebook.objects.get(pk=id)
                        except Gradebook.DoesNotExist:
                            raise Http404(f"Missing gradebook for '{gradebook.user}'")
                        else:
                            gradebook.grade = float(request.POST[item])
                            gradebook.save()

    return HttpResponseRedirect(reverse("course-detail", kwargs={"code": code}))


@user_passes_test(is_teacher)
def course_delete(request, code):
    """
    For course deletion
    CONSTRAINT: Only the teacher who created the course can delete it.
    """
    try:
        course = Course.objects.get(code=code)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    else:
        # Allow deletion only if the user is the teacher of the course
        if request.user == course.teacher:
            course.delete()
        # View should not exist for non-teachers
        else:
            raise Http404('Not Found.')

    return HttpResponseRedirect(reverse("user-index"))
