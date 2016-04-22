#coding:utf-8
__author__ = 'similarface'
from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name=forms.CharField(max_length=25,label='姓名    ')
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea,label='备注')

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')

class SearchForm(forms.Form):
    '''
    查询框
    '''
    query=forms.CharField(label='关键字')

