from typing import Set
from django.contrib import admin

from exam.models import  Answer, ExamTime, Exams, Paper, Question

# Register your models here.
# admin.site.register(Student)
admin.site.register(Exams)
admin.site.register(Question)
admin.site.register(Paper)
admin.site.register(ExamTime)
admin.site.register(Answer)