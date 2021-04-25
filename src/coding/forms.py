#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
----------------------------------------------------------------------------------------------------
* Project Name : SQL_memOJi
* File Name    : forms.py
* Description  : Django Forms
* Create Time  : 2021-04-25 16:36:39
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh/SQL_memOJi
----------------------------------------------------------------------------------------------------
* Notice
- 
- 
----------------------------------------------------------------------------------------------------
'''


from django.forms import ModelForm
from django.forms import widgets as wid
from django.utils.translation import gettext_lazy as _
import coding.models


class QuesSetForm(ModelForm):
    '''For coding/questions-manage.html'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' ' + ' '.join([
                    'form-control',
                ])
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                })

    class Meta:
        model = coding.models.QuestionSet

        fields = [
            'ques_set_name',
            'initiator',
            'ques_set_desc',
            'create_sql',
        ]

        error_messages = {
            # 'xxx': {'required': _("xxx不能为空"), },
        }

        widgets = {
            'ques_set_desc': wid.Textarea(attrs={'rows': 3}),
            'create_sql': wid.Textarea(attrs={'rows': 8}),
            'initiator': wid.Select(attrs={'class': 'select2'}),
        }


class QuestionForm(ModelForm):
    '''For coding/questions-manage.html'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' ' + ' '.join([
                    'form-control',
                ])
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                })

    class Meta:
        model = coding.models.Question

        fields = [
            'ques_name',
            'initiator',
            'ques_set',
            'ques_difficulty',
            'ques_desc',
            'ques_ans',
        ]

        error_messages = {
            # 'xxx': {'required': _("xxx不能为空"), },
        }

        widgets = {
            'initiator': wid.Select(attrs={'class': 'select2'}),
            'ques_set': wid.Select(attrs={'class': 'select2'}),
            'ques_difficulty': wid.Select(attrs={'class': 'select2'}),
            'ques_desc': wid.Textarea(attrs={'rows': 3}),
            'ques_ans': wid.Textarea(attrs={'rows': 3}),
        }