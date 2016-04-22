#coding:utf-8
from django.shortcuts import render
#404
from django.shortcuts import get_object_or_404
#分页模块
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
# Create your views here.
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm
#邮件模块
from django.core.mail import send_mail
from django.db.models import Count

#标签
from taggit.models import Tag
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def post_list(request,tag_slug=None):
    '''
    文章的列表
    :param request:
    :return:所有文章的列表
    '''
    #获取所有的published的文章

    object_list=Post.published.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        object_list=object_list.filter(tags__in=[tag])
    paginator=Paginator(object_list,3)
    #rquest没有就返回None
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    return render(request,'myblog/post/list.html',{'page':page,'posts':posts,'tag':tag})


def post_detail(request,year,month,day,post):
    '''
    文章详情
    +
    评论详情
    :param request:
    :param year:文章发布的年份
    :param month:文章发布的月份
    :param day:文章发布day
    :param post:文章标题
    :return:匹配的具体对象
    '''
    post=get_object_or_404(Post,title=post)
    #post.comments 的来源 ==> related_name='comments'
    comments=post.comments.filter(active=True)
    new_comment=None
    if request.method=='POST':
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            #不会存入数据库
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()
    else:
        comment_form=CommentForm()
    # 列出相似的文章
    #获取文章post的标签
    post_tags_ids = post.tags.values_list('id', flat=True)
    #过滤其他的文章排除本事
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    #
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags',
                                                                             '-publish')[:4]
    return render(request,'myblog/post/detail.html',{'post':post,
                                                     'comments': comments,
                                                     'comment_form':comment_form,
                                                     'new_comment':new_comment,
                                                     'similar_posts': similar_posts
                                                     })

def post_share(request,post_id):
    '''
    文章分享 发送邮件
    '''
    post=get_object_or_404(Post,id=post_id,status='published')
    sent=False
    if request.method=='POST':
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) 推荐你阅读 "{}"'.format(cd['name'], cd['email'], post.title)
            message = '阅读: "{}" 地址: {}\n\n{}\ 备注: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            #这儿的yangwubing@23mofang.com 要和settings.py的EMAIL_HOST_USER 对应
            send_mail(subject, message, 'yangwubing@23mofang.com',[cd['to']])
            sent = True
    else:
        form=EmailPostForm()
    return render(request, 'myblog/post/share.html', {'post': post,'form': form,'sent': sent})


class PostListView(ListView):
    '''
    对象列表返回类 分页 包装
    '''
    #查询结果集
    queryset = Post.published.all()
    #对象容器
    context_object_name = 'posts'
    #分页大小
    paginate_by = 3
    #定向到那个模版
    template_name = 'myblog/post/list.html'


from .forms import SearchForm
from haystack.query import SearchQuerySet
# def post_serarch(request):
#     '''
#     文章搜索
#     :param request:
#     :return:
#     '''
#     form = SearchForm()
#     if 'query' in request.GET:
#         form=SearchForm(request.GET)
#         if form.is_valid():
#             cd=form.cleaned_data
#             results=SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
#             total_results=results.count()
#             for result in results:
#                 pass
#
#             return render(request,'myblog/post/search.html',{'form':form,'cd':cd,'results':results,'total_results':total_results})
#     return render(request,'myblog/post/search.html',{'form':form})

def post_search(request):
    '''
    文章搜索
    :param request:
    :return:
    '''
    form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post).filter(content=cd['query'])#.load_all()
            #.load_all()
            # count total results
            total_results = results.count()
            for result in results:
                a=result.object

            return render(request, 'myblog/post/search.html', {'form': form,
                                                     'cd': cd,
                                                     'results': results,
                                                     'total_results': total_results})
    return render(request, 'myblog/post/search.html', {'form': form})
