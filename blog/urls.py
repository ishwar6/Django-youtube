
from django.contrib import admin
from django.urls import path

from posts.views import show_post, homepage, detail, post_create, subject_sidebar, login_

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', show_post, name='post-show'),
    path('posts/create', post_create, name='post-create'),
    path('', homepage),

    path('posts/<slug:post_id>', detail),
    path('subject/<int:id>', subject_sidebar),
      path('login', login_, name='login'),
]


#  path('posts/<slug:slug>', detail),
