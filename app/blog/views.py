from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from .models import Category, Article
from .serializers import CategorySerializer, ArticleSerializer, ArticleListSerializer, ArticleCreateSerializer
from accounts.permissions import IsAuthorOrReadOnly


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class ArticleListCreateView(generics.ListCreateAPIView):
    serializer_class = ArticleListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Article.objects.all()
        search = self.request.query_params.get('search', None)
        category_id = self.request.query_params.get('category_id', None)
        author_id = self.request.query_params.get('author_id', None)
        is_published = self.request.query_params.get('is_published', None)
        sort_field = self.request.query_params.get('sort', 'created_at')  # 默认按created_at排序
        order = self.request.query_params.get('order', 'desc')  # 默认倒序
        queryset = queryset.filter(is_published=True)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(summary__icontains=search)
            )

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if author_id:
            queryset = queryset.filter(author_id=author_id)

        if is_published is not None:
            is_published_bool = is_published.lower() == 'true'
            queryset = queryset.filter(is_published=is_published_bool)
        if order == 'desc':
            sort_field = f'-{sort_field}'
        queryset = queryset.order_by(sort_field)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ArticleCreateSerializer
        return ArticleListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 增加浏览次数
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserArticleListView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_articles(request):
    query = request.GET.get('q', '')
    if not query:
        return Response({'error': '搜索关键词不能为空'}, status=status.HTTP_400_BAD_REQUEST)

    articles = Article.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(summary__icontains=query)
    ).filter(is_published=True).order_by('-created_at')

    serializer = ArticleListSerializer(articles, many=True)
    return Response({
        'items': serializer.data,
        'total': articles.count(),
        'page': 1,
        'size': len(serializer.data),
        'pages': 1
    })