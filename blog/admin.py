from django.contrib import admin
from .models import Post, Comment
# Register your models here.
# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'published_date', 'post_status')
    list_filter = ('post_status', 'published_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    raw_id_fields = ('author',)
    ordering = ['post_status', '-published_date']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_at', 'active']
    list_filter = ['active', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'body']