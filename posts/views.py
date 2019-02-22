from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
# Create your views here.
import datetime
from .models import Post, Subject
from django.urls import reverse
from .forms import PostCreate, LoginForm
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from django.urls import reverse

from django.views.generic import DetailView, ListView, UpdateView


class PostListAll(ListView):
    model = Post
    template_name = 'posts/all.html'
    context_object_name = 'posts'

    def queryset(self):
        return Post.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['date'] = datetime.datetime.now()
        return context


def post_list(request):
    all_posts = Post.objects.all()
    context = {
        'posts': all_posts,
        'date': datetime.datetime.now()
    }
    return render(request, 'posts/all.html', context)


def show_post(request):

    q = Post.objects.all()

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
    if request.user.is_authenticated:

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
                    user=request.user,
                    title=title,
                    blog_type=blog_type,
                    text=text,
                    status=status
                )
                return redirect('post-show')
            else:
                return render(request, 'posts/create.html', context)
    else:
        return redirect('accounts:login')


def subject_sidebar(request, id):
    subject = get_object_or_404(Subject, id=id)
    posts = subject.post_set.all()
    context = {
        'time': datetime.datetime.now(),
        'posts': posts
    }
    return render(request, 'posts/posts.html', context)


def post_update_new(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        print(post)

        if post.user != request.user:
            return HttpResponse('<h1>Permission Denied</h1>')
        form = PostCreate(instance=post)

        if request.method == 'POST':
            post = get_object_or_404(Post, id=post_id)
            form = PostCreate(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                blog_type = form.cleaned_data.get('blog_type')
                text = form.cleaned_data.get('text')
                status = form.cleaned_data.get('status')

                post.title = title
                post.blog_type = blog_type
                post.text = text
                post.status = status
                post.save()
                return redirect('post-show')

        return render(request, 'posts/update.html', {'form': form})
    else:
        return redirect('accounts:login')


def login_(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print('here')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if username and password:
                print('here 2')
                user_obj = authenticate(
                    request, username=username, password=password)
                print(user_obj)
                if user_obj is not None:
                    login(request, user_obj)
                    return redirect('post-show')
    return render(request, 'posts/update.html', {'form': form})


class PostList(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'

    def queryset(self, *args, **kwargs):
        return Post.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/details.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['subjects'] = Subject.objects.all()
        return context


class PostCreateNew(CreateView):
    model = Post
    form_class = PostCreate
    template_name = 'posts/create.html'

    def get_success_url(self):
        return reverse('post-show')


class PostUpdate(UpdateView):
    model = Post

    template_name = 'posts/create.html'
    fields = ('status', 'title', 'text', 'blog_type')

    def get_success_url(self):
        return reverse('post-show')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print(context)
        return context
