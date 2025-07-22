from django.contrib import admin
from .models import Student, Session, StudentClass, Section, FeeReport, FeeDefaulter, AttendanceReport

admin.site.register(Student)
admin.site.register(Session)
admin.site.register(StudentClass)
admin.site.register(Section)
admin.site.register(FeeReport)
admin.site.register(FeeDefaulter)
admin.site.register(AttendanceReport)
