from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('students/', views.students_list, name='students_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/bulk_delete/', views.bulk_delete_students, name='bulk_delete_students'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.add_attendance, name='add_attendance'),
    path('fee_reports/', views.fee_reports_list, name='fee_reports_list'),
    path('fee_reports/add/', views.add_fee_report, name='add_fee_report'),
    path('defaulters/', views.defaulters_list, name='defaulters_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
]