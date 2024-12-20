from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('courses/', views.course_list, name="course_list"),
    path('', views.all_students, name="all_students"),
    path('csv', views.export_model_csv, name="export_model_csv"),
    path('pdf',views.export_model_pdf, name="export_model_pdf"),
    path('all', views.StudentsListView.as_view(), name = "all_students2"),
    path('all/<int:pk>', views.StudentDetailView.as_view(), name = 'single_student'),
    
]