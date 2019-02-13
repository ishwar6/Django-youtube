
from django.contrib import admin
from django.urls import path, include

from posts.views import show_post, homepage, detail, post_create, subject_sidebar,  login_, post_update_new

from posts.views import PostList, PostDetail, PostCreateNew, PostUpdate


from django.conf import settings


from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', show_post, name='post-show'),
    path('posts/create', post_create, name='post-create'),
    path('', homepage),

    path('posts/<slug:post_id>', detail, name='post-detail'),
    path('subject/<int:id>', subject_sidebar),
    path('post/update/<int:post_id>', post_update_new, name='post-update'),
    path('login', login_, name='login'),

    path('blogs/', include('posts.urls', namespace='blog')),
<<<<<<< HEAD
    path('products/', include('product.urls', namespace='product')),

    path('cart/', include('cart.urls', namespace='cart')),
    path('account/', include('accounts.urls', namespace='accounts')),
=======
>>>>>>> 542bfc8a32b0feee925334932b25bfc4701f3498


    # class based views


<<<<<<< HEAD
    # path('class/posts', PostList.as_view(), name='all-posts'),
    # path('class/posts/<slug:slug>', PostDetail.as_view(), name='c-post'),

    # path('class/post/create', PostCreate.as_view(), name='c-post'),
    # path('class/post/update/<int:pk>', PostUpdate.as_view(), name='c-update'),
=======
    path('class/posts', PostList.as_view(), name='all-posts'),
    path('class/posts/<slug:slug>', PostDetail.as_view(), name='c-post'),

    path('class/post/create', PostCreate.as_view(), name='c-post'),
    path('class/post/update/<int:pk>', PostUpdate.as_view(), name='c-update'),
>>>>>>> 542bfc8a32b0feee925334932b25bfc4701f3498



]


#  path('posts/<slug:slug>', detail),

if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
