from ast import For
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    STUDENT = "STU"
    TEACHER = "TEA"
    ROLE_CHOICES = [
        (STUDENT, "Student"),
        (TEACHER, "Teacher"),
    ]
    role = models.CharField(max_length=3, choices=ROLE_CHOICES, default=STUDENT)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Course(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=60, unique=True)
    title = models.CharField(max_length=255)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teaching")
    students = models.ManyToManyField(User, related_name="attending", blank=True)

    def __str__(self):
        return f"{self.code}"


class Gradebook(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="gradebooks"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="gradebooks"
    )
    grade = models.FloatField(null=True, blank=True)


# Additional ideas, but I didn't implement them anymore because I hope to apply for a job soon.
"""
class Task(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.title


class Submission(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="submissions"
    )
    file = models.FileField(upload_to="files/%Y/%m/%d")
    comment = models.CharField(max_length=500, null=True, blank=True)
    grade = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.task.course.code}: {self.task.title} by {self.student}"
"""
