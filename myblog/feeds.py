#coding:utf-8
__author__ = 'similarface'

from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

class LastestPostsFeed(Feed):
    title='博客园'
    link='/myblog'
    description='新的文章'
    def items(self):
           return Post.published.order_by('-publish')[:5]
    def item_title(self, item):
           return item.title
    def item_description(self, item):
           return truncatewords(item.content, 30)


