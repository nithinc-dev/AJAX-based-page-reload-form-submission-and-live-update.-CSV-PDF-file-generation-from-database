from django.contrib import admin
from studentApp.models import Student,Course,Enrollment

# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    search_fields = ("name",)
class StudentAdmin(admin.ModelAdmin):
    list_filter = ("name","usn")
    search_fields = ("name","usn")
    
class EnrollmentAdmin(admin.ModelAdmin):
    list_filter = ("enrollment_date",)
    ordering = ("-enrollment_date",)
    
admin.site.register(Student,StudentAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Enrollment,EnrollmentAdmin)