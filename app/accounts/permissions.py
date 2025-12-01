from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    自定义权限：只有作者可以编辑自己的文章
    """

    def has_object_permission(self, request, view, obj):
        # 读取权限对所有请求开放
        if request.method in permissions.SAFE_METHODS:
            return True

        # 写入权限只对文章作者开放
        return obj.author == request.user

    def has_permission(self, request, view):
        # GET/HEAD/OPTIONS请求（查询文章列表）允许所有人
        if request.method in permissions.SAFE_METHODS:
            return True
        # POST请求（创建文章）需要登录
        return request.user and request.user.is_authenticated