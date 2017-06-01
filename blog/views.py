from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Post,MyModel_text,MyModel,Archive
from django.utils import timezone
from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect,HttpResponse
from .forms import PostForm,MyForm
from .forms import UploadFileForm
from django.db.models import Q
import json
from django.urls import reverse
from .forms import FileFieldForm
from django.http import HttpResponseRedirect
import os

from markdownx.utils import markdownify
from comments.forms import CommentForm

# Create your views here.
def test(request):
    return render(request, 'blog/base.html')


def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    archives=Archive.objects.all()
    return render(request,'blog/post_list.html',{'archives':archives,'posts':posts})

def post_list_archive(request,archive_name):
    arc=Archive.objects.filter(Archive_name=archive_name)
    posts=Post.objects.filter(Archive=arc).all()
    archives=Archive.objects.all()
    return  render(request,'blog/post_list_archive.html',{'archives':archives,'posts':posts})
    # return HttpResponse("www.baidu.com")
    # pass

def post_detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
               'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request,'blog/post_detail.html',context=context)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            post.text=markdownify(request.POST.get('markdown'))
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        # form=MyForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect(post_detail,pk=post.pk)

    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_search(request):
    q = request.GET.get('q')

    if not q:
        return render(request, 'blog/post_list.html', )

    post_list = Post.objects.filter(Q(text__icontains=q) | Q(title__icontains=q))
    return render(request, 'blog/post_list.html',{'posts':post_list })

def lab(request):
    if request.method=="POST":
        form = MyForm(request.POST)
        print("ok")
        if form.is_valid():
            print("ok")
            test=MyModel_text.objects.create()
            test.mytext=request.POST.get('myfield')
            test.save()
            text=markdownify(test.mytext)
            print(text)
            return render(request,'blog/test.html',{'text':text})
    else:
        myform = MyForm()
    return render(request,'blog/lab.html',{'form':myform})

def upload_file(request):
    if request.method=='POST':
        form=UploadFileForm(request.POST,request.FILES)
        # form=UploadFileForm(request.POST,request.FILES.getlist("files"))

        if form.is_valid():
            # for count,x in enumerate(request.FILES.getlist("files")):
            #     handle_uploaded_file(count,x)
            handle_uploaded_file(request.FILES['file'],request.FILES['file'].name)

            return render(request,'blog/lab/success.html')
    else:
        form=UploadFileForm()
    return render(request, 'blog/lab/upload_file.html')

# def handle_uploaded_file(count,f):
#         print(count)

def handle_uploaded_file(f,name):

    with open('./media/'+str(name)+'.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def about_me(request):
    return render(request,'blog/aboutme.html')

@csrf_exempt
def scene_update_view(request):
    if request.method == "POST":
            # name = request.POST.get('name')
            print(request.POST)
            status = 0
            result = "Error!"
            return HttpResponse("ok")
            # return HttpResponse(json.dumps({
            #     "status": status,
            #     "result": result
            # }))