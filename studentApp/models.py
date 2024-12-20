from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Student(models.Model):
    usn = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    courses = models.ManyToManyField(Course, through='Enrollment')

    def __str__(self):
        return self.name

#one student can have many enrolments, therfore one to maany (foreign key)
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"
    
    