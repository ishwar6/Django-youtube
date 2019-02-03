from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
# Create your views here.
import datetime
from .models import Post, Subject
from django.urls import reverse
from .forms import PostCreate


def show_post(request):
    print('haha')

    q = Post.objects.all()
    print(q)
    print(request.method)
    context = {
        'time': datetime.datetime.now(),
        'posts': q
    }
    return render(request, 'posts/posts.html', context)


def detail(request, post_id):
    q = Post.objects.filter(slug=post_id)
    all_subjects = Subject.objects.all()
    if q.exists():
        q = q.first()
    else:
        return HttpResponse('<h1>Page Not Found</h1>')

    context = {

        'post': q,
        'subjects': all_subjects
    }

    return render(request, 'posts/details.html', context)


def _detail(request, slug):

    q = Post.objects.filter(slug__iexact=slug)
    if q.exists():
        q = q.first()
    else:
        return HttpResponse('<h1>Post Not Found</h1>')
    context = {

        'post': q
    }
    return render(request, 'posts/details.html', context)


def homepage(request):
    return HttpResponse('<h1>Homepage</h1>')


def post_create(request):

    if request.method == 'GET':
        form = PostCreate()
        context = {
            'form': form
        }
        return render(request, 'posts/create.html', context)

    else:
        form = PostCreate(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            blog_type = form.cleaned_data.get('blog_type')
            text = form.cleaned_data.get('text')
            status = form.cleaned_data.get('status')

            Post.objects.create(
                title=title,
                blog_type=blog_type,
                text=text,
                status=status
            )
            return redirect('post-show')
        else:
            return render(request, 'posts/create.html', context)


def subject_sidebar(request, id):
    subject = get_object_or_404(Subject, id=id)
    posts = subject.post_set.all()
    context = {
        'time': datetime.datetime.now(),
        'posts': posts
    }
    return render(request, 'posts/posts.html', context)