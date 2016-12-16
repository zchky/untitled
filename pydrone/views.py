
# Create your views here.
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from django.http import HttpResponse
from django.shortcuts import render
from .forms import AddForm
from .models import testdata


def index(request):
    return render(request,'pydrone/index.html')

def main(request):
    return render(request,'pydrone/the_main.html')

def push(request):
    return render(request,'pydrone/push.html')

def base(request):
    return render(request,'pydrone/base.html')

def online_plot(request):
    return render(request,'pydrone/online_plot.html')

def online_map(request):
    return render(request,'pydrone/online_map.html')

def offline_plot(request):
    if request.method == 'POST':  # 当提交表单时

        form = AddForm(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            c=testdata.objects.filter(time__gt=a,time__lt=b)

            return  HttpResponse(c.all().values())
        else:
            return  HttpResponse(4)


    else:  # 当正常访问时
        return render(request,'pydrone/offline_plot.html')

def offline_map(request):
    return  render(request,'pydrone/offline_map.html')

# def add(request):
#     a = request.GET['a']
#     b = request.GET['b']
#     a = int(a)
#     b = int(b)
#     return HttpResponse(str(a+b))