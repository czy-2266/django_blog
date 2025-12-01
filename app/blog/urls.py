from django.urls import path
from . import views, views_upload

urlpatterns = [
    # 分类管理
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # 文章管理
    path('articles/', views.ArticleListCreateView.as_view(), name='article-list-create'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('users/me/articles/', views.UserArticleListView.as_view(), name='user-article-list'),
    
    # 文章搜索
    path('articles/search/', views.search_articles, name='article-search'),
    
    # 文件上传
    path('upload/', views_upload.upload_file, name='upload-file'),
    path('upload/multiple/', views_upload.upload_file, name='upload-multiple'),
    path('users/me/avatar/', views_upload.upload_file, name='upload-avatar'),
]