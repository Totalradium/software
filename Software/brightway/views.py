from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from datetime import datetime
from django.db.models import Sum, Count
from .models import Student, Employee, FeeReport, AttendanceReport, FeeDefaulter, AcademicCalendarEvent
from .forms import StudentForm, AttendanceReportForm, FeeReportForm, EmployeeForm

def index(request):
    now = datetime.now()
    total_students = Student.objects.count()
    students_this_month = Student.objects.filter(date_of_birth__month=now.month).count()
    total_employees = Employee.objects.count()
    employees_this_month = Employee.objects.filter(id__isnull=False).count()  # Replace with actual logic

    revenue = FeeReport.objects.filter(status='paid').aggregate(total=Sum('student__fee_amount'))['total'] or 0
    revenue_this_month = FeeReport.objects.filter(status='paid', month=now.strftime('%B')).aggregate(total=Sum('student__fee_amount'))['total'] or 0

    profit = revenue  # Replace with actual profit calculation
    profit_this_month = revenue_this_month  # Replace with actual profit calculation

    estimated_fee = FeeReport.objects.filter(month=now.strftime('%B')).aggregate(total=Sum('student__fee_amount'))['total'] or 0
    collections = FeeReport.objects.filter(status='paid', month=now.strftime('%B')).aggregate(total=Sum('student__fee_amount'))['total'] or 0
    remainings = FeeReport.objects.filter(status='not_paid', month=now.strftime('%B')).aggregate(total=Sum('student__fee_amount'))['total'] or 0

    # Chart data
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    chart_labels = months
    chart_expenses = [FeeReport.objects.filter(month=m, status='not_paid').aggregate(total=Sum('student__fee_amount'))['total'] or 0 for m in months]
    chart_income = [FeeReport.objects.filter(month=m, status='paid').aggregate(total=Sum('student__fee_amount'))['total'] or 0 for m in months]

    context = {
        'total_students': total_students,
        'students_this_month': students_this_month,
        'total_employees': total_employees,
        'employees_this_month': employees_this_month,
        'revenue': revenue,
        'revenue_this_month': revenue_this_month,
        'profit': profit,
        'profit_this_month': profit_this_month,
        'estimated_fee': estimated_fee,
        'collections': collections,
        'remainings': remainings,
        'chart_labels': chart_labels,
        'chart_expenses': chart_expenses,
        'chart_income': chart_income,
    }
    return render(request, 'brightway/index.html', context)
# Create your views here.
def hello(request):
    return HttpResponse("Hello World")
def job(request,id):
    return HttpResponse(f"This is the {id} job page")
def students_list(request):
    students = Student.objects.all()
    return render(request, 'brightway/students_list.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students_list')
    else:
        form = StudentForm()
    return render(request, 'brightway/add_student.html', {'form': form})

def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'brightway/edit_student.html', {'form': form})

def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('students_list')
    return render(request, 'brightway/delete_student.html', {'student': student})

def attendance_list(request):
    attendance_reports = AttendanceReport.objects.all()
    return render(request, 'brightway/attendance_list.html', {'attendance_reports': attendance_reports})

def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceReportForm()
    return render(request, 'brightway/add_attendance.html', {'form': form})

def fee_reports_list(request):
    fee_reports = FeeReport.objects.all()
    return render(request, 'brightway/fee_reports_list.html', {'fee_reports': fee_reports})

def add_fee_report(request):
    if request.method == 'POST':
        form = FeeReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fee_reports_list')
    else:
        form = FeeReportForm()
    return render(request, 'brightway/add_fee_report.html', {'form': form})

def defaulters_list(request):
    defaulters = FeeDefaulter.objects.all()
    return render(request, 'brightway/defaulters_list.html', {'defaulters': defaulters})

def bulk_delete_students(request):
    if request.method == 'POST':
        ids = request.POST.getlist('selected_students')
        Student.objects.filter(id__in=ids).delete()
    return redirect('students_list')

def academic_calendar(request):
    events = AcademicCalendarEvent.objects.all()
    return render(request, 'brightway/academic_calendar.html', {'events': events})

def absentees_chart(request):
    # Example: Absentees by grade for current month
    from django.db.models import Count
    now = datetime.now()
    absentees = AttendanceReport.objects.filter(
        status='absent',
        date__month=now.month
    ).values('grade').annotate(count=Count('id'))
    # Prepare data for chart
    chart_data = {item['grade']: item['count'] for item in absentees}
    return render(request, 'brightway/absentees_chart.html', {'chart_data': chart_data})

def add_employee(request):
    # You need to create an EmployeeForm in forms.py
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees_list')
    else:
        form = EmployeeForm()
    return render(request, 'brightway/add_employee.html', {'form': form})