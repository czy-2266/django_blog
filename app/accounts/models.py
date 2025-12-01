from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    #输出魔法方法 本来这里print或者调用应该是一个object对象 但是有了这个魔法方法 就会返回魔法方法中return的内容
    #更改显示
    def __str__(self):
        return self.username