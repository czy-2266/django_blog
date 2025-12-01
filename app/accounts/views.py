from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User
from .serializers import UserSerializer
import re
from django.db.models import F

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    用户注册
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # 验证输入
    if not username or not password:
        return Response({'error': '用户名和密码是必填项'}, status=status.HTTP_400_BAD_REQUEST)

    # 验证用户名格式
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return Response({'error': '用户名格式不正确，应为3-20位字母、数字或下划线'}, status=status.HTTP_400_BAD_REQUEST)

    # 验证邮箱格式（如果提供了邮箱）
    if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return Response({'error': '邮箱格式不正确'}, status=status.HTTP_400_BAD_REQUEST)

    # 验证密码强度
    # try:
    #     validate_password(password)
    # except ValidationError as e:
    #     return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

    # 检查用户名是否已存在
    if User.objects.filter(username=username).exists():
        return Response({'error': '用户名已被注册'}, status=status.HTTP_400_BAD_REQUEST)

    # 检查邮箱是否已存在（如果提供了邮箱）
    if email and User.objects.filter(email=email).exists():
        return Response({'error': '邮箱已被注册'}, status=status.HTTP_400_BAD_REQUEST)

    # 创建用户 objects管理器 增删改查方法 不需要再手动save保存
    # user = User.objects.create_user43w(username=username, email=email, password=password)
    # user = User.objects.create(username=username, email=email, password=password)
    user, created = User.objects.get_or_create(username=username, email=email, password=password)#防止重复数据添加包错，有不执行添加操作 反之
    # 如果用户已存在，返回错误
    if not created:
        return Response({'error': '用户名已被注册'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 设置密码并保存用户
    if password:
        user.set_password(password)
        user.save()
        
    serializer = UserSerializer(user)
    return Response({
        'user': serializer.data,
        'message': '注册成功'
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):

    """
    用户登录
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': '用户名和密码是必填项'}, status=status.HTTP_400_BAD_REQUEST)
    # 数据查询all方法 返回的是 Queryset 查询集（数据记录） 【（模型对象），（模型对象）】查询所有
    # res=User.objects.all()
    # res=User.objects.all().values()#values()转字典

    # get条件查询 得到符合条件的单条模型对象
    # res=User.objects.get(username=username,password=password)

    # filter条件查询得到的是查询集 queryset 【（模型对象）】
    # res=User.objects.filter(username=username)

    #模糊查询 name__icontains参数：则是忽略大小写 name__startswith:查询开头 name__endswith:查询结尾 name是可以变的按照数据库表字段来
    #xx__range:区间查询  xx__in:查询xx字段在指定的内容的数据
    #xx__gt：大于 xx_lt:小于 xx_lte:小于等于 xx__gte:大于等于
    # res = User.objects.filter(name__contains='张')

    # 排序 字段名 正序 -字段名 倒叙
    # res=User.objects.order_by('-age')

    # first（）第一条数据 last()最后一条数据
    # res=User.objects.first()

    # F 针对某一个字段进行全部修改
    # res = User.objects.all().update(age = F('age')+1)

    #修改某一个字段的内容
    # res = User.objects.get(username=username)
    # res.username = 'xxx'
    # res.save()

    #方法二
    # res = User.objects.filter(username__icontains='xxx').update(password=1234)

    #方法一 删除
    # res = User.objects.filter(username=username).delete()


    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        return Response({'error': '用户已禁用'}, status=status.HTTP_400_BAD_REQUEST)

    # 创建或获取token
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({
        'user': serializer.data,
        'token': token.key
    })


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    """
    获取或更新当前用户信息
    """
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            # 检查用户名是否已存在
            username = request.data.get('username')
            if username and username != user.username:
                if User.objects.filter(username=username).exists():
                    return Response({'error': '用户名已被使用'}, status=status.HTTP_400_BAD_REQUEST)

            # 检查邮箱是否已存在
            email = request.data.get('email')
            if email and email != user.email:
                if User.objects.filter(email=email).exists():
                    return Response({'error': '邮箱已被使用'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)