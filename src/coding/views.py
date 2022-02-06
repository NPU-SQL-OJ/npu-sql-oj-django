#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : views.py
* Description  : 
* Create Time  : 2021-04-04 00:46:48
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh/SQL_memOJi
----------------------------------------------------------------------------------------------------
* Notice
- 
- 
----------------------------------------------------------------------------------------------------
'''


import pymysql
from django.shortcuts import render, redirect
from django.urls import Resolver404
from django.views import View
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.db.models import Sum
from prettytable import PrettyTable
from coding import forms
from coding import models
from utils import token as tk
from utils import sql_check
from django.db.models import Q
from django.utils import timezone

# Create your views here.


def exams_manage(request):
    '''Render exams-manage template'''

    exam_form = forms.ExamForm(auto_id='id_exam_%s')
    exer_form = forms.ExerciseForm(auto_id='id_exer_%s')

    exams_list = models.Exam.objects.order_by('publish_time')
    exer_list = models.Exercise.objects.order_by('publish_time')
    next_exam = exams_list.first()

    content = {
        'exam_form': exam_form,
        'exer_form': exer_form,
        'exams_list': exams_list,
        'exer_list': exer_list,
        'next_exam': next_exam,
    }

    return render(request, 'coding/exams-manage.html', context=content)


def exam_add(request):
    '''Add exams in exams-manage page'''

    exam_form = forms.ExamForm(request.POST)

    if exam_form.is_valid():
        exam_form.save()

    return redirect('coding:exams-manage')


def exer_add(request):
    '''Add exercises in exams-manage page'''

    exer_form = forms.ExerciseForm(request.POST)

    if exer_form.is_valid():
        exer_form.save()

    return redirect('coding:exams-manage')

#------------------------------------Questions Manage Page-----------------------------------#


def questions_manage_base(request):
    '''Render questions-manage-base template'''

    ques_set_form = forms.QuesSetForm(auto_id='id_qset_%s')
    question_form = forms.QuestionForm(auto_id='id_ques_%s')
    paper_form = forms.PaperForm(auto_id='id_paper_%s')

    question_list = models.Question.objects.all()
    ques_set_list = models.QuestionSet.objects.all()
    paper_list = models.Paper.objects.all()

    content = {
        'ques_set_form': ques_set_form,
        'question_form': question_form,
        'paper_form': paper_form,
        'question_list': question_list,
        'ques_set_list': ques_set_list,
        'paper_list': paper_list,
    }

    return render(request, 'coding/questions-manage-base.html', context=content)
# XXX(Seddon Shen):need to modify the user control logic more
def questions_manage(request):
    '''Render questions-manage template'''

    ques_set_form = forms.QuesSetForm(auto_id='id_qset_%s')
    question_form = forms.QuestionForm(auto_id='id_ques_%s')
    paper_form = forms.PaperForm(auto_id='id_paper_%s')
    question_list = models.Question.objects.filter(initiator_id=request.user.email)
    ques_set_list = models.QuestionSet.objects.filter(initiator_id=request.user.email)
    paper_list = models.Paper.objects.filter(initiator_id=request.user.email)

    questions_cnt = models.Question.objects.filter(initiator_id=request.user.email).count()
    # print(questions_cnt)
    # print(question_list.values())



    content = {
        'ques_set_form': ques_set_form,
        'question_form': question_form,
        'paper_form': paper_form,
        'question_list': question_list,
        'ques_set_list': ques_set_list,
        'paper_list': paper_list,
        'questions_cnt': questions_cnt
    }

    return render(request, 'coding/questions-manage.html', context=content)


# XXX(Steve X): database grants for teachers
def ques_set_add(request):
    '''Add question set in questions-manage page'''

    ques_set_form = forms.QuesSetForm(request.POST)
    host = tk.get_conf('mysql', 'host')
    port = int(tk.get_conf('mysql', 'port'))
    user = tk.get_conf('mysql', 'user')
    passwd = tk.get_conf('mysql', 'password')

    db = pymysql.Connect(host=host, port=port, user=user, passwd=passwd)
    cur = db.cursor()
    qset_db_name = f'qset_{request.POST.get("db_name")}'
    create_sql = request.POST.get('create_sql').replace('\n', '').replace('\\n', '')
    create_sql_list = create_sql.split(';')

    # print(create_sql)
    # print(type(create_sql))
    # print('-'*40)
    # print(create_sql_list)

    try:
        cur.execute(f"""create database {qset_db_name};""")
        cur.execute(f"""use {qset_db_name};""")

        for sql in create_sql_list:
            cur.execute(sql)

        db.commit()
        if ques_set_form.is_valid():
            ques_set_form.save()

        # FIXME(Steve X): db_name 重名问题
        qset = models.QuestionSet.objects.get(db_name=ques_set_form.cleaned_data.get('db_name'))
        qset.db_name = qset_db_name
        qset.save()
    except Exception as exc:
        cur.execute(f"""drop database if exists {qset_db_name}""")
        db.rollback()
        print(exc)

    cur.close()
    db.close()

    return redirect('coding:questions-manage')


def question_add(request):
    '''Add question in questions-manage page'''

    question_form = forms.QuestionForm(request.POST)

    if question_form.is_valid():
        question_form.save()

    return redirect('coding:questions-manage')


# FIXME(Steve X): date time picker
def paper_add(request):
    '''Add paper in questions-manage page'''

    paper_form = forms.PaperForm(request.POST)

    if paper_form.is_valid():
        paper_form.save()
    else:
        print(paper_form.errors)

    return redirect('coding:questions-manage')
#--------------------------------------------END---------------------------------------------#


def coding(request):
    '''Render coding template'''
    conditions = {
        'classroom' : request.user.student.classroom,
        'active' : True
    }
    exams_list = models.Exam.objects.order_by('publish_time').filter(**conditions)
    exer_list = models.Exercise.objects.order_by('publish_time').filter(**conditions)
    have_finished = models.PaperAnswerRec.objects.filter(student=request.user.student)
    have_finished_paper = []
    for element in have_finished:
        have_finished_paper.append(element.paper_id)
    unfinished = exams_list.exclude(paper_id__in=have_finished_paper)
    have_finished = models.Exam.objects.order_by('publish_time').filter(paper_id__in=have_finished_paper)
    next_exam = unfinished.first()
    content = {
        'exams_list': unfinished,
        'finished' : have_finished,
        'exer_list': exer_list,
        'next_exam': next_exam,
    }

    return render(request, 'coding/coding.html', context=content)


class CodingEditor(View):
    '''Render coding-editor template'''
    # 今天读了一下审题逻辑 Seddon 2021/12/30
    def get_info(self, request, event_type, event_id, ques_id):
        try:
            question = models.Question.objects.get(ques_id=ques_id)
            qset = question.ques_set
            # print("Question:",question,"Qset:",qset)
            if event_type == 'exam':
                # print("Exam")
                event = models.Exam.objects.get(exam_id=event_id)
                event_name = event.exam_name
                # print("Event_name:",event_name)
            elif event_type == 'exer':
                # print("Exercise")
                event = models.Exercise.objects.get(exer_id=event_id)
                event_name = event.exer_name
            else:
                raise Resolver404
        except:
            raise Resolver404

        # Previous & next question id
        prev_question = event.paper.question.filter(ques_id__lt=ques_id).order_by('-ques_id').first()
        next_question = event.paper.question.filter(ques_id__gt=ques_id).order_by('ques_id').first()
        now_paperquestion = models.PaperQuestion.objects.get(Q(question=question) & Q(paper=event.paper))
        host = tk.get_conf('mysql', 'host')
        port = int(tk.get_conf('mysql', 'port'))
        user = tk.get_conf('mysql', 'user')
        passwd = tk.get_conf('mysql', 'password')
        db = pymysql.Connect(host=host, port=port, user=user, passwd=passwd)
        cur = db.cursor()

        # Create PrettyTable for `show tables;`
        pt_db_tables = PrettyTable(['Tables in this database'])
        pt_db_tables.align = 'l'
        cur.execute(f'''use {qset.db_name};''')
        cur.execute(f'''show tables;''')
        tables = [tb[0] for tb in cur.fetchall()]
        pt_db_tables.add_rows([[tb] for tb in tables])

        # Create PrettyTable for `desc <table_name>;`
        tables_desc = [str(pt_db_tables)]
        for tb in tables:
            cur.execute(f'''desc {tb};''')
            pt_table_desc = PrettyTable(['Field', 'Type'])
            pt_table_desc.align = 'l'
            pt_table_desc.add_rows([row[:2] for row in cur.fetchall()])
            tables_desc.append('\n' + tb)
            tables_desc.append(str(pt_table_desc))

        db_desc = '\n'.join(tables_desc)
        cur.close()
        db.close()

        content = {
            'event': event,
            'event_id': event_id,
            'event_type': event_type,
            'event_name': event_name,
            'question': question,
            'paperquestion':now_paperquestion,
            'db_desc': db_desc,
            'prev_question': prev_question if prev_question else None,
            'next_question': next_question if next_question else None,
        }
        # 判断一下是否是用户首次做这个题 去查表
        cur_user = request.user
        if cur_user.is_authenticated:
            if event_type == 'exam':
                exam = models.Exam.objects.get(pk=event_id)    
                rec = models.ExamQuesAnswerRec.objects.filter(user=cur_user, question=question, exam=exam).first()
            elif event_type == 'exer':
                exer = models.Exercise.objects.get(pk=event_id)
                rec = models.ExerQuesAnswerRec.objects.filter(user=cur_user, question=question, exer=exer).first()
            else:
                raise Resolver404
            if rec:
                correct = rec.ans_status
                if correct == 0 :
                    correct_bool = True
                elif correct == 1:
                    correct_bool = False
                else:
                    correct_bool = 'error'
                ans_status_color = {
                    True: 'success',
                    False: 'danger',
                    'error': 'warning',
                }.get(correct_bool)
                content.update({
                    'correct': correct_bool,
                    'ans_status_color': ans_status_color,
                    'submit_ans': rec.ans,
                })

        return content

    def get(self, request, event_type, event_id, ques_id):
        '''Show info'''

        content = self.get_info(request, event_type, event_id, ques_id)
        if ques_id == '1':
            cur_user = request.user
            if cur_user.is_authenticated:
                if event_type == 'exam':
                    # print('是考试')
                    exam = models.Exam.objects.get(pk=event_id)
                    rec = models.ExamAnswerRec.objects.filter(student=cur_user.student, exam=exam).first()
                    if rec is None:
                        models.ExamAnswerRec.objects.create(
                            student=cur_user.student,
                            exam=exam,
                            start_time = timezone.now()
                        )
                        # print("创建成功")
                    # else:
                    #     print("已存在记录")

                else:
                    # print("是练习")
                    exer = models.Exercise.objects.get(pk=event_id)
                    rec = models.ExerAnswerRec.objects.filter(student=cur_user.student, exer=exer).first()
                    if rec is None:
                        models.ExerAnswerRec.objects.create(
                            student=cur_user.student,
                            exer=exer,
                            start_time = timezone.now()
                            # question=question,
                            # ans=submit_ans,
                            # ans_status=ans_status,
                            # submit_cnt=1,
                        )
                    # else:
                    #     print("已存在记录")
        return render(request, 'coding/coding-editor.html', context=content)

    def post(self, request, event_type, event_id, ques_id):
        '''Submit SQL'''

        # FIXME(Steve X): Monaco Editor 输入内容换行会消失
        submit_ans = request.POST.get('submit_ans')
        # print("输入的答案:",submit_ans)
        content = self.get_info(request, event_type, event_id, ques_id)
        question = content.get('question')
        qset = question.ques_set
        # print("数据比对:",qset.db_name,question.ques_ans,submit_ans)
        try:
            submit_ans = '#' if submit_ans == '' else submit_ans
            correct = sql_check.ans_check(db_nm=qset.db_name, ans_sql=question.ques_ans, stud_sql=submit_ans)
            # print("判断动作执行成功")
        except Exception as e:
            print(e)
            correct = 'error'

        ans_status = {
            True: models.QuesAnswerRec.AnsStatus.AC,
            False: models.QuesAnswerRec.AnsStatus.WA,
            'error': models.QuesAnswerRec.AnsStatus.RE,
        }.get(correct)

        ans_status_color = {
            True: 'success',
            False: 'danger',
            'error': 'warning',
        }.get(correct)

        # Question-Answer record
        cur_user = request.user
        # print(event_type)
        if cur_user.is_authenticated:
            if event_type == 'exam':
                exam = models.Exam.objects.get(pk=event_id)    
                rec = models.ExamQuesAnswerRec.objects.filter(user=cur_user, question=question, exam=exam).first()
            elif event_type == 'exer':
                exer = models.Exercise.objects.get(pk=event_id)
                rec = models.ExerQuesAnswerRec.objects.filter(user=cur_user, question=question, exer=exer).first()
            else:
                raise Resolver404
            if rec:
                rec.ans_status = ans_status
                rec.submit_cnt += 1
                rec.ans = submit_ans
                if ans_status == 0:
                    if event_type == 'exam':
                        event = models.Exam.objects.get(exam_id=event_id)
                    elif event_type == 'exer':
                        event = models.Exercise.objects.get(exer_id=event_id)
                    else:
                        raise Resolver404
                    now_paperquestion = models.PaperQuestion.objects.get(Q(question=question) & Q(paper=event.paper))
                    # print(now_paperquestion.score)
                    rec.score = now_paperquestion.score
                else:
                    rec.score = 0
                    #XXX:(Seddon)把一道正确的题再交错，到底是按正确的还是错误的分数，有待商榷
                rec.save()
            else:
                if event_type == 'exam':
                    models.ExamQuesAnswerRec.objects.create(
                        user=cur_user,
                        question=question,
                        ans=submit_ans,
                        ans_status=ans_status,
                        submit_cnt=1,
                        exam=exam,
                        score=0
                    )
                elif event_type == 'exer':
                    models.ExerQuesAnswerRec.objects.create(
                        user=cur_user,
                        question=question,
                        ans=submit_ans,
                        ans_status=ans_status,
                        submit_cnt=1,
                        exer=exer,
                        score=0
                    )
                else:
                    raise Resolver404

        content.update({
            'correct': correct,
            'ans_status_color': ans_status_color,
            'submit_ans': submit_ans,
        })

        return render(request, 'coding/coding-editor.html', context=content)


def statistics(request):
    '''Render statistics template'''

    ques_cnt = models.Question.objects.count()
    ques_set_cnt = models.QuestionSet.objects.count()
    exam_cnt = models.Exam.objects.count()
    exam_active = models.Exam.objects.filter(active=True).count()
    exer_cnt = models.Exercise.objects.count()
    # exer_active = models.Exercise.objects.filter().count()
    submit_cnt = models.QuesAnswerRec.objects.aggregate(Sum('submit_cnt'))
    ac_cnt = models.QuesAnswerRec.objects.filter(ans_status=0).count()
    exer_active = models.Exercise.objects.filter(active=True).count()
    content = {
        'ques_cnt': ques_cnt,
        'ques_set_cnt': ques_set_cnt,
        'exam_cnt': exam_cnt,
        'exam_active': exam_active,
        'exer_cnt': exer_cnt,
        'exer_active': exer_active,
        'submit_cnt': submit_cnt['submit_cnt__sum'],
        'ac_cnt' : ac_cnt
    }

    return render(request, 'coding/statistics.html', context=content)
