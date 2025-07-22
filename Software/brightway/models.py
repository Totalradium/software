from django.db import models
import re
from django.core.exceptions import ValidationError

# Create your models here.

def validate_session_name(value):
    if not re.match(r'^\d{4}-\d{4}$', value):
        raise ValidationError('Session name must be in format YYYY-YYYY (e.g., 2025-2026)')

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    roll_no = models.PositiveIntegerField(unique=True)
    student_class = models.ForeignKey('StudentClass', on_delete=models.CASCADE, related_name='students')
    section = models.ForeignKey('Section', on_delete=models.CASCADE, related_name='students')
    fee_amount = models.PositiveIntegerField(default=0)  # Add this field
    date_of_birth = models.DateField(null=True, blank=True)  # New field

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_no})"


class Session(models.Model):
    session_name = models.CharField(
        max_length=9, 
        unique=True, 
        validators=[validate_session_name]
    )

    def __str__(self):
        return self.session_name


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StudentClass(models.Model):
    name = models.CharField(max_length=50)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='classes')
    subjects = models.ManyToManyField(Subject, related_name='classes')

    def __str__(self):
        return f"{self.name} ({self.session.session_name})"


class Section(models.Model):
    name = models.CharField(max_length=10)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return f"{self.name} ({self.student_class.name} - {self.student_class.session.session_name})"


class FeeReport(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('not_paid', 'Not Paid'),
    ]
    MONTH_CHOICES = [
        ('January', 'January'),('February', 'February'), ('March', 'March'),
        ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'),
        ('August', 'August'), ('September', 'September'), ('October', 'October'),
        ('November', 'November'), ('December', 'December'),
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='fee_reports')
    session = models.ForeignKey('Session', on_delete=models.CASCADE, related_name='fee_reports')
    month = models.CharField(max_length=9, choices=MONTH_CHOICES)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student} - {self.month} - {self.status}"


class FeeDefaulter(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='fee_defaulters')
    fee_report = models.ForeignKey('FeeReport', on_delete=models.CASCADE, related_name='defaulter_entry')

    def __str__(self):
        return f"{self.student} (Defaulter)"

    @staticmethod
    def update_defaulters(session, month):
        unpaid_reports = FeeReport.objects.filter(status='not_paid', session=session, month=month)
        FeeDefaulter.objects.all().delete()
        for report in unpaid_reports:
            FeeDefaulter.objects.create(student=report.student, fee_report=report)

class AttendanceReport(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='attendance_reports')
    date = models.DateField()
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    grade = models.CharField(max_length=2, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"


# Utility function for monthly income
def get_monthly_income(session, month):
    paid_reports = FeeReport.objects.filter(status='paid', session=session, month=month)
    return sum(report.student.fee_amount for report in paid_reports)

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    date_of_joining = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AcademicCalendarEvent(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    event_type = models.CharField(max_length=50, choices=[('holiday', 'Holiday'), ('exam', 'Exam'), ('other', 'Other')])

    def __str__(self):
        return f"{self.title} on {self.date}"


class SidebarMenu(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    icon_class = models.CharField(max_length=100, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='submenus', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Sidebar Menu'
        verbose_name_plural = 'Sidebar Menus'