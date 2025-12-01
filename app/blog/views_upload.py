from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import uuid
import os
from django.conf import settings
from django.http import HttpResponse


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    """
    文件上传
    """
    if 'file' not in request.FILES:
        return Response({'error': '没有上传文件'}, status=status.HTTP_400_BAD_REQUEST)

    uploaded_file = request.FILES['file']

    # 检查文件类型
    allowed_types = {
        'image/jpeg', 'image/png', 'image/gif', 'image/webp',
        'application/pdf', 'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    }

    if uploaded_file.content_type not in allowed_types:
        return Response({'error': '不支持的文件类型'}, status=status.HTTP_400_BAD_REQUEST)

    # 检查文件大小（10MB限制）
    if uploaded_file.size > 10 * 1024 * 1024:
        return Response({'error': '文件大小不能超过10MB'}, status=status.HTTP_400_BAD_REQUEST)

    # 生成唯一文件名
    file_extension = os.path.splitext(uploaded_file.name)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    # 确保上传目录存在
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    # 保存文件
    file_path = os.path.join(upload_dir, unique_filename)
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    # 构建文件URL
    file_url = f"{settings.MEDIA_URL}uploads/{unique_filename}"

    return Response({
        'filename': unique_filename,
        'original_filename': uploaded_file.name,
        'file_url': file_url,
        'file_size': uploaded_file.size,
        'file_type': uploaded_file.content_type
    })