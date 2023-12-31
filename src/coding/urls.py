#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : urls.py
* Description  : 
* Create Time  : 2021-04-05 11:32:17
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh/SQL_memOJi
----------------------------------------------------------------------------------------------------
* Notice
- 
- 
----------------------------------------------------------------------------------------------------
'''


from django.urls import path
from . import views
from . import apis

app_name = 'coding'
urlpatterns = [
    # Management Pages
    # path('exams-manage/', views.exams_manage, name='exams-manage'),
    # path('exams-manage/exam-add/', views.exam_add, name='exam-add'),
    # path('exams-manage/exer-add/', views.exer_add, name='exer-add'),
    path('coding/', views.coding, name='coding'),
    path('coding-editor/<event_type>/<event_id>/<ques_id>/', views.CodingEditor.as_view(), name='coding-editor'),
    path('statistics/', views.statistics, name='statistics'),

    # Questions-Manage Page
    # path('questions-manage-base/', views.questions_manage_base, name='questions-manage-base'),
    # path('questions-manage/', views.questions_manage, name='questions-manage'),
    # path('questions-manage/ques-set-add/', views.ques_set_add, name='ques-set-add'),
    # path('questions-manage/question-add/', views.question_add, name='question-add'),
    # path('questions-manage/paper-add/', views.paper_add, name='paper-add'),

    # # APIs
    # path('api/test/', apis.test_api, name='api-test'),
    # path('api/question-list/', apis.question_list, name='question-list'),


    # Analysis
    path('analysis/<event_type>/<event_id>/', views.PaperDetails.as_view(), name='paper-analysis'),
    path('teacheranalysis/<event_type>/<event_id>/', views.ExamExerTeacherDetails.as_view(), name='teacher-analysis'),
]
