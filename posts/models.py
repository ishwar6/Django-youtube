from django.db import models

from django.db.models.signals import pre_save, post_save
# from authors.models import Author
from blog.utils import unique_slug_generator


class Subject(models.Model):
    title = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, null=True, blank=True)
   # author = models.OneToOneField(
    # Author, on_delete = models.CASCADE, blank = True, null = True)
    blog_type = models.ForeignKey(Subject, on_delete=models.CASCADE)
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


# def pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)

# pre_save.connect(pre_save_receiver, sender=Post)
