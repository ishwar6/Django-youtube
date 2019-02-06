
from .views import PostListAll, post_list
from django.urls import path


app_name = 'posts'

urlpatterns = [

    path('list', PostListAll.as_view(), name='list'),

    path('f-list', post_list, name='f-list'),
]
