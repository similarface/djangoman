#coding:utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
#标签包
# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    '''
    实体－文章类
    发布的文章
    '''
    STATUS_CHOICES={
        ('draft', '草稿'),
           ('published', '发布'),
    }
    title=models.CharField(max_length=300,verbose_name='文章标题')
    zhaiyao=models.TextField(verbose_name='摘要')
    content=models.TextField(verbose_name='文章内容')
    author = models.ForeignKey(User,related_name='blog_posts')
    publish = models.DateTimeField(default=timezone.now,verbose_name='发布时间')
    created = models.DateTimeField(auto_now_add=True,verbose_name='提交时间')
    updated = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    status=models.CharField(max_length=10,choices=STATUS_CHOICES)
    objects=models.Manager()
    tags=TaggableManager
    published=PublishedManager()
    # #分类标签
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('myblog:post_detail',args=[self.publish.year,
                                self.publish.strftime('%m'),
                                self.publish.strftime('%d'),
                                self.title.encode('utf-8')])

class Comment(models.Model):
    '''
    文章的评论
    '''
    #一对多的关系 一个文章有多条评论 评论的主体来自文章
    post = models.ForeignKey(Post, related_name='comments')
    #名称
    name = models.CharField(max_length=80)
    #邮件
    email = models.EmailField()
    #评论内容
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

