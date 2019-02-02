from django.contrib import admin

# Register your models here.


from .models import Post, Subject


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'blog_type')
    list_filter = ('title', 'blog_type')
    search_fields = ('title',)
    ordering = ('id',)


admin.site.register(Subject)
