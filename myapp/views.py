from django.shortcuts import render
from django.http import HttpResponse
from . models import articlePost
import markdown
# Create your views here.

def article_list(request):
	articles=articlePost.objects.all()

	return render(request,'article/list.html',{'articles':articles})
	
def article_detail(request,id):
	article=articlePost.objects.get(id=id)
	article.body=markdown.markdown(article.body,
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        ])

	return render(request,'article/detail.html',{'article':article})