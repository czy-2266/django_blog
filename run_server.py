import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    # 运行Django开发服务器
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8002'])