from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def homepage(request):
	context='一定可以的，相信自己，别人花一年，我可以花两年时间'
	return render(request,'flexx/homepage.html',{'context':context})