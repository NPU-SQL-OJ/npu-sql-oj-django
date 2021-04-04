#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : views.py
* Description  : 
* Create Time  : 2021-04-04 00:43:27
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh/SQL_memOJi
----------------------------------------------------------------------------------------------------
* Notice
- 
- 
----------------------------------------------------------------------------------------------------
'''


from django.shortcuts import render

# Create your views here.


def base(request):
    '''Render base template'''

    return render(request, 'base.html')


def blank(request):
    '''Render blank template'''

    return render(request, 'pages-starter.html')


def auth_base(request):
    '''Render auth-base template'''

    return render(request, 'user/auth-base.html')


def auth_login(request):
    '''Render auth-login template'''

    return render(request, 'user/auth-login.html')


def auth_recoverpw(request):
    '''Render auth-recoverpw template'''

    return render(request, 'user/auth-recoverpw.html')


# def home(request):
#     '''Render home page'''

#     return render(request, 'user/home.html')
