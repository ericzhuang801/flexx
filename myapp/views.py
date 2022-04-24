from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from . forms import articlepostform
from . models import articlePost
import markdown
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from comment.models import articleComment
# Create your views here.

def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    if search:
        if order == 'total_views':
            # 用 Q对象 进行联合搜索
            article_list = articlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = articlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ''
        if order == 'total_views':
            article_list = articlePost.objects.all().order_by('-total_views')
        else:
            article_list = articlePost.objects.all()
	
    paginator=Paginator(article_list,3)
    page=request.GET.get('page')
    articles=paginator.get_page(page)
    return render(request,'article/list.html',{'articles':articles,'order':order,'search':search})
	
def article_detail(request,id):
	article=articlePost.objects.get(id=id)
	comments = articleComment.objects.filter(article=id)
	md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ]
    )
	article.body = md.convert(article.body)
	article.total_views += 1
	article.save(update_fields=['total_views'])
	return render(request,'article/detail.html',{'article':article,'toc':md.toc,'comments':comments})

@login_required(login_url='/userprofile/login/')
def article_create(request):
	if request.method=='POST':
		article_post_form=articlepostform(data=request.POST)
		if article_post_form.is_valid():
			new_article = article_post_form.save(commit=False)
			new_article.author=User.objects.get(id=request.user.id)
			new_article.save()
			return redirect('myapp:article_list')
		else:
			return HttpResponse("表单内容有误，请重新填写")
	else:
		article_post_form=articlepostform()
		context={'article_post_form':article_post_form}
		return render(request,'article/create.html',context)

@login_required(login_url='/userprofile/login/')
def article_safe_delete(request,id):
	if request.method=='POST':

		article=articlePost.objects.get(id=id)
		article.delete()
		return redirect('myapp:article_list')
	else:
		return HttpResponse("仅允许post请求")

@login_required(login_url='/userprofile/login/')
def article_update(request,id):
	article= articlePost.objects.get(id=id)
	if request.user != article.author:
		return HttpResponse("抱歉，你无权修改这篇文章。")
	if request.method=='POST':
		article_post_form=articlepostform(data=request.POST)
		if article_post_form.is_valid():
			article.title=request.POST['title']
			article.body=request.POST['body']
			article.save()
			return redirect("myapp:article_detail",id=id)
		else:
			return HttpResponse("表单有误，请重新填写")
	else:
		article_post_form=articlepostform()
		context={'article':article,'article_post_form':article_post_form}
		return render(request,'article/update.html',context)