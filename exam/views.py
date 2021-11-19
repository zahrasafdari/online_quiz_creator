from django.contrib.auth.models import User
from django.http.response import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, QuestionForm, RegisterForm
from .models import Answer, ExamTime, Paper, Question
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    register_form = RegisterForm(request.POST or None)
    if register_form.is_valid():
        user_name = register_form.cleaned_data.get('user_name')
        password = register_form.cleaned_data.get('password')
        email = register_form.cleaned_data.get('email')
        User.objects.create_user(
            username=user_name, email=email, password=password)
        return redirect('/login')

    context = {
        'register_form': register_form
    }
    return render(request, 'register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        user_name = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            login_form.add_error(
                'username', 'کاربری با این مشخصات وجود ندارد')
    context = {
        'login_form': login_form
    }
    return render(request, 'login.html', context)


@login_required(login_url='/login')
def start_exam(request):
    papers = Paper.objects.filter(student_name_id=request.user.id,is_finished=False)
    if papers is not None:
        context = {
            'papers': papers
        }
        return render(request, 'start_exam.html', context)


def logout_request(request):
    logout(request)
    return redirect("/login")


@login_required(login_url='/login')
def answer(request, *args, **kwargs):
    selected_paper_id = kwargs['paperId']
    data = request.POST
    anslist = []
    queid_list = []

    if request.method == 'GET':
        exam_time_start = ExamTime.objects.filter(
            paper=selected_paper_id).first()
        exam_time_start.start_time = datetime.now()
        exam_time_start.save()
        paper = Paper.objects.filter(
            id=selected_paper_id,
            student_name=request.user.id,
            is_finished=False
            ).first()
        if paper is not None:
            questions = Question.objects.filter(
                question_paper_id=selected_paper_id
            )
            questionform_list = []

            for question in questions:
                form = QuestionForm(question)
                questionform_list.append(form)
            context = {'formlist': questionform_list,
                    'ques': questions}

            return render(request, 'exam.html', context)
        else:
            return HttpResponseNotFound("This page is not found") 

    if request.method == 'POST':
        paper = Paper.objects.filter(id=selected_paper_id).first()
        exam_time_finish = ExamTime.objects.filter(
            paper=selected_paper_id).first()
        exam_time_finish.finish_time = datetime.now()
        exam_time_finish.save()
        exam_time_start = ExamTime.objects.filter(
            paper=selected_paper_id).first()
        exam_time_finish1 = ExamTime.objects.filter(
            paper=selected_paper_id).first()
        print(exam_time_start.start_time)
        print(exam_time_finish.finish_time)
        timedelta = exam_time_finish1.finish_time - exam_time_start.start_time
        timedelta_in_s = timedelta.total_seconds()
        minutes = divmod(timedelta_in_s, 60)[0]
        
        time_minute = paper.time_minute

        if minutes < time_minute:
            for k, v in data.items():
                anslist.append(v)
                queid_list.append(k[7:])
            ans_id = dict(zip(queid_list[1:], anslist[1:]))

            for queid, ans in ans_id.items():
                the_question = Question.objects.filter(id=queid).first()
                student_answer = Answer.objects.create(
                    student_id=request.user.id,
                    related_paper_id=selected_paper_id,
                    question_related_id=queid,
                    student_answer=ans
                )
                student_choice = student_answer.student_answer
                correct_ans = the_question.answer
                if student_choice == correct_ans:
                    student_answer.is_correct = True
                    student_answer.save()
            total_mark = Answer.objects.filter(
                related_paper=selected_paper_id, is_correct=True
            ).aggregate(
                total_result=Sum('question_related__marks')
            )['total_result']
            paper.is_finished=True
            paper.save()
            context = {
                'total_score': total_mark,
                'ans_list': anslist[1:]
            }

            return render(request, 'result.html', context)

        else:
            return render(request, 'time_finished_error.html', {})
