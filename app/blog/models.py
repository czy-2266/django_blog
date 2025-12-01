from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default="#409EFF")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.CharField(max_length=500, blank=True, null=True)
    cover_image = models.ImageField(upload_to='article_covers/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='articles')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


class ArticleAttachment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='attachments')
    filename = models.CharField(max_length=255,blank=True, null=True)
    original_filename = models.CharField(max_length=255,blank=True, null=True)
    file_path = models.CharField(max_length=500)
    file_size = models.IntegerField()
    file_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.filename