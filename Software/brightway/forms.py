from django import forms
from .models import Student, AttendanceReport, FeeReport

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class AttendanceReportForm(forms.ModelForm):
    class Meta:
        model = AttendanceReport
        fields = '__all__'

class FeeReportForm(forms.ModelForm):
    class Meta:
        model = FeeReport
        fields = '__all__'
        
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = FeeReport
        fields = '__all__'
        