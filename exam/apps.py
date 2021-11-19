from django.apps import AppConfig
from django.db import models

class QuestionOption(models.TextChoices):
        option1= 'option1', ('A')
        option2 = 'option2', ('B')
        option3 = 'option3', ('C')
        option4 = 'option4', ('D')
        noans = '', ('')
class ExamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exam'


