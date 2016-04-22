#coding:utf-8
__author__ = 'similarface'
from django import template
from django.db.models import Count
register=template.Library()
from  ..models import Post
from django.utils.safestring import mark_safe
import markdown

@register.simple_tag()
def total_posts():
    '''
    文章总数
    :return:返回发布的文章总篇数
    '''
    return Post.published.count()


@register.inclusion_tag('myblog/post/latest_posts.html')
def show_latest_posts(count=5):
    '''
    最新count篇文章
    :param count: 文章的篇数 默认5篇
    :return:最新count篇文章的对象
    '''
    latest_posts=Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.assignment_tag
def get_most_commented_posts(count=5):
    '''
    返回评论最多的前count篇文章
    :param count:默认为5
    :return:返回评论最多的前count篇文章
    '''
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

