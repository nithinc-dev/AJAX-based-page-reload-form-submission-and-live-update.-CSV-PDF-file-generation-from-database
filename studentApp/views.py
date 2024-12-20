from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import Course, Student, Enrollment
from .forms import StudentForm, CourseForm
from django.db.models import Count,Q
from django.contrib import messages
from django.http import HttpResponse

def register(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            usn = form.cleaned_data['usn']
            if Student.objects.filter(usn=usn).exists():
                response = "<h3>Student already registered</h3>"
            else:
                form.save()
                response = "<h3>Your form has been submitted successfully!</h3>"
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return HttpResponse(response)
            else:
                messages.success(request, response)
                return redirect('register')
    else:
        form = StudentForm()
    
    return render(request, 'ajax_student_registration.html', {'form': form})



# def register(request):
#     if request.method == "POST":
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             usn = form.cleaned_data['usn']
#             if Student.objects.filter(usn=usn).exists():
#                 return HttpResponse("<h3>Student already registered</h3>")
#             else:
#                 form.save()
#                 messages.success(request, "Your form has been submitted successfully!")
                
#                 return redirect('register')  # Redirect to the same view function
#     else:
#         form = StudentForm()
    
#     return render(request, 'ajax_student_registration.html', {'form': form})

# def register(request):
#     if request.method == "POST":
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Your form has been submitted successfully !")
#             return redirect('register') #redirect to the same view function
#     else:
#         form = StudentForm()
#     return render(request, 'student_registration.html', {'form': form})



#  if form.save() == True:
#                 form.save()
#                 messages.success(request, "Your form has been submitted successfully !")
#                 return redirect('register') #redirect to the same view function
#             else:
#                 messages.success(request, "Failed!, Please enter proper credentials and try again")
#     else:
#         form = StudentForm()
#     return render(request, 'student_registration.html', {'form': form})

def course_list(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            enrollments = Enrollment.objects.filter(course=course)
            # count_students_enrolled_to_that_course = Enrollment.objects.aggregate(Count(course=course))
            # count_students_enrolled_to_that_course = Enrollment.objects.aggregate(Count('course', filter=Q(course=course)))['course__count']
            count_students_enrolled_to_that_course = enrollments.count()
            return render(request, 'ajax_course_list.html', {'course': course, 
                                                             'enrollments': enrollments, 
                                                             'count': count_students_enrolled_to_that_course})
    else:
        form = CourseForm()
    return render(request, 'ajax_course_list.html', {'form': form})



from django.http import JsonResponse

def all_students(request):
    students = Student.objects.all().values('id', 'name', 'usn')
    return JsonResponse({'students': list(students)})

# def all_students(request):
#     enrollment()
#     students = Student.objects.all()
#     return render(request, 'ajax_all_students.html', {'students': students})

from django.views.generic import ListView, DetailView

class StudentsListView(ListView):
    template_name = 'ajax_all_students.html'
    model = Student
    context_object_name = 'students'

class StudentDetailView(DetailView):
    template_name = 'single_student.html'
    model = Student
    
    # def get_context_data(self, **kwargs):
    #      context =  super().get_context_data(**kwargs)
    #      s_id = self.kwargs.get("pk")
    #      selected_student = Student.objects.get(pk=s_id)
    #      context['student'] = selected_student
    #      return context
   
import csv
from django.http import HttpResponse 


def export_model_csv(request):
    # usually http response will send html now we are changing the content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="enrollment.csv"'
    writer = csv.writer(response)
    #heading
    writer.writerow(['Student', 'Course', 'Date'])
    enrollments = Enrollment.objects.all().values_list('student__name', 'course__name', 'enrollment_date')
    # the output may be [[student,course,date],[],[],[]]
    # enrollments = Enrollment.objects.select_related('student', 'course').values_list(
    #     'student__name', 'course__name', 'enrollment_date')
    #enrollments = Enrollment.objects.select_related('student', 'course')
    # for enrollment in enrollments:         
    #     writer.writerow([enrollment.student.name, enrollment.course.name, enrollment.enrollment_date])
    for row in enrollments:
        writer.writerow(row)
        #it takes list as input 
    return response

def enrollment():
    enrollments = Enrollment.objects.all()
    for i in enrollments:
        print(i)
# from django.http import HttpResponse 
# from django.template.loader import get_template 
# from xhtml2pdf import pisa
# def export_model_pdf(request):
#     enrollments = Enrollment.objects.all() 

#     context = {'enrollment': enrollments} 

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="enrollment.pdf"'
#     template = get_template('enrollment.pdf') 
#     html = template.render(context) 
#     pisa_status = pisa.CreatePDF( 
#     html, dest=response) 
#     if pisa_status.err: 
#         return HttpResponse('We had some errors <pre>' + html + '</pre>') 
    
    
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Enrollment
from django.utils import timezone


def export_model_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="enrollment_data.pdf"'
   
    # Create a BytesIO buffer to receive the PDF data.
    # buffer = BytesIO()
   
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(response)
   
    # Draw the title
    p.drawString(100, 750, "Student Enrollment Data")
   
    # Fetch data from the model
    data = Enrollment.objects.all()
    # data = Enrollment.objects.all().select_related('student', 'course')
   
    # Set starting position for the data
    y = 720
    line_height = 20
   
    # Write data to the PDF
    for entry in data:
        p.drawString(100, y, f"Name: {entry.student.name}, Course: {entry.course.name}, Enrollment-date: {entry.enrollment_date}")
        y -= line_height
       
        # Check if we need to move to a new page
        if y < 50:
            p.showPage()
            y = 750
   
    # Close the PDF object cleanly.
    p.showPage()
    p.save()
   
    # Get the value of the BytesIO buffer and write it to the response.
    # pdf = buffer.getvalue()
    # buffer.close()
    # response.write(pdf)
   
    return response


# def export_model_pdf(request):
#     # Create the HttpResponse object with the appropriate PDF headers.
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="enrollment_data.pdf"'
   
#     # Create a BytesIO buffer to receive the PDF data.
#     buffer = BytesIO()
   
#     # Create the PDF object, using the buffer as its "file."
#     p = canvas.Canvas(buffer)
   
#     # Draw the title
#     p.drawString(100, 750, "Student Enrollment Data")
   
#     # Fetch data from the model
#     data = Enrollment.objects.all()
#     # data = Enrollment.objects.all().select_related('student', 'course')
   
#     # Set starting position for the data
#     y = 720
#     line_height = 20
   
#     # Write data to the PDF
#     for entry in data:
#         p.drawString(100, y, f"Name: {entry.student.name}, Course: {entry.course.name}, Enrollment-date: {entry.enrollment_date}")
#         y -= line_height
       
#         # Check if we need to move to a new page
#         if y < 50:
#             p.showPage()
#             y = 750
   
#     # Close the PDF object cleanly.
#     p.showPage()
#     p.save()
   
#     # Get the value of the BytesIO buffer and write it to the response.
#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)
   
#     return response




#     # views.py
# from django.http import HttpResponse
# from reportlab.pdfgen import canvas
# from io import BytesIO
# from . models import *

# def export_model_pdf(request):
#     # Create the HttpResponse object with the appropriate PDF headers.
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="data.pdf"'
    
#     # Create a BytesIO buffer to receive the PDF data.
#     buffer = BytesIO()
    
#     # Create the PDF object, using the buffer as its "file."
#     p = canvas.Canvas(buffer)
    
#     # Draw the title
#     p.drawString(100, 750, "SpO2 and BPM Data")
    
#     # Fetch data from the model
#     data = Enrollment.objects.all()
    
#     # Set starting position for the data
#     y = 720
#     line_height = 20
    
#     # Write data to the PDF
#     for entry in data:
#         p.drawString(100, y, f"Name: {entry.student.name}, Course: {entry.course__name}, Enrollment-date: {entry.enrollment_date}")
#         y -= line_height
        
#         # Check if we need to move to a new page
#         if y < 50:
#             p.showPage()
#             y = 750
    
#     # Close the PDF object cleanly.
#     p.showPage()
#     p.save()
    
#     # Get the value of the BytesIO buffer and write it to the response.
#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)
    
#     return response

    
    
    
    
    
    
    
# def export_model_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="enrollment.csv" '
#     writer = csv.writer(response)
#     writer.writerow([ 'Student', 'Course', 'Date'])
#     enrollments = Enrollment.objects.all().values_list('Student.name', 'Course.name', 'enrollment_date')
#     for row in enrollments:
#         writer.writerow(row)
#     return response
    
    