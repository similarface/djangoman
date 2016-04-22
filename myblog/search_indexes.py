#coding:utf-8
__author__ = 'similarface'

from haystack import indexes
from .models import Post
class PostIndex(indexes.SearchIndex,indexes.Indexable):
    '''
    给文章Post 建立索引
    '''
    text = indexes.CharField(document=True, use_template=True)
    publish = indexes.DateTimeField(model_attr='publish')
    def get_model(self):
        return Post
    def index_queryset(self, using=None):
        return self.get_model().published.all()
