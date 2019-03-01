from django.urls import reverse
from blog.utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save
import os
import random
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# from authors.models import Author


class Subject(models.Model):
    title = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/subject/id'


STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)


def upload_image_path_posts(instance, filename):
    new_filename = random.randint(1, 9910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "posts/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, null=True, blank=True)
   # author = models.OneToOneField(
    # Author, on_delete = models.CASCADE, blank = True, null = True)
    blog_type = models.ForeignKey(Subject, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=upload_image_path_posts, null=True, blank=True)
    text = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-published_at',)

    def __str__(self):
        return self.title


def save_title_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(save_title_slug, sender=Post)
