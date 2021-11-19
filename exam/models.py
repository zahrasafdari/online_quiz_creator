
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from .apps import  QuestionOption
from django.utils import timezone


# class Student(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE,db_constraint=False)
#     def __str__(self):
#         return str(self.user)

class QuestionsManager(models.Manager):
    def get_by_id(self, product_id):
        qs = self.get_queryset().filter(id=product_id)
        if qs.count() == 1:
            return qs.first()
        else:
            return None

class Exams(models.Model):
    exam_name = models.CharField(max_length=500)
    

    def __str__(self):
        return self.exam_name

class Paper(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    student_name=models.ForeignKey(User,on_delete=models.CASCADE,db_constraint=False)
    paper_exam_name = models.ForeignKey(Exams, on_delete=models.CASCADE)
    time_minute=models.PositiveIntegerField(default=0)
    question_nums=models.PositiveIntegerField(default=0)
    is_finished=models.BooleanField()
    
    def __str__(self):
        return str(self.id)

class Question(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    question_exam_name = models.ForeignKey(Exams, on_delete=models.CASCADE)
    question_paper=models.ForeignKey(Paper,on_delete=models.CASCADE,related_name='question_paper',db_constraint=False)
    question_text=models.TextField()

    marks = models.PositiveIntegerField(default=0)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100, choices=QuestionOption.choices)

    def __str__(self):
        return str(self.question_text)

class Answer(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,related_name='student_answer_set',db_constraint=False)
    related_paper=models.ForeignKey(Paper,on_delete=models.CASCADE,related_name='related_paper',db_constraint=False)
    question_related=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='Qusetion_related')
    student_answer=models.CharField(max_length=100, choices=QuestionOption.choices)
    is_correct=models.BooleanField(default=False)
    mark=models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.question_related)

class ExamTime(models.Model):
    paper=models.ForeignKey(Paper,on_delete=models.CASCADE,db_constraint=False)
    start_time=models.DateTimeField(default=timezone.now)
    finish_time=models.DateTimeField(default=timezone.now)