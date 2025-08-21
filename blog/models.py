from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(post_status=PostStatus.PUBLISHED)
    
class PostStatus(models.TextChoices):
    DRAFT = 'DF', 'Draft'
    PUBLISHED = 'PB', 'Published'
    # ARCHIVED = 'archived', 'Archived'
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique_for_date='published_date')
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)  # Default to now and i am in confusion about the use case
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post_status = models.CharField(max_length=10, choices=PostStatus.choices, default=PostStatus.DRAFT)

    objects = models.Manager()  # Default manager
    published = PublishedManager()  # Custom manager for published posts
    
    tags = TaggableManager() # this tag manager will allow to add, retrieve, and remove tags from the post objects.

    class Meta:
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['-published_date']),
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[
            self.published_date.year,           # :02 can be used for zero padding
            self.published_date.month,
            self.published_date.day,
            self.slug
            ])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]  

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"  


    