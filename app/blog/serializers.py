from rest_framework import serializers
from blog.models import Category, Article, ArticleAttachment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'color', 'creator', 'created_at']
        read_only_fields = ['creator', 'created_at']


class ArticleAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleAttachment
        fields = ['id', 'filename', 'original_filename', 'file_path', 'file_size', 'file_type', 'uploaded_at']


class ArticleListSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'summary', 'cover_image', 'is_published', 'views_count', 
                  'author', 'author_username', 'category', 'category_name', 'created_at', 'updated_at']


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'summary', 'cover_image', 'is_published', 
                  'category', 'created_at', 'updated_at']


class ArticleSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    attachments = ArticleAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'summary', 'cover_image', 'is_published', 'views_count',
                  'author', 'author_username', 'category', 'category_name', 'created_at', 'updated_at', 'attachments']