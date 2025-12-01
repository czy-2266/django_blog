#!/usr/bin/env python
"""
项目启动脚本
"""
import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def start_backend():
    """启动Django后端"""
    print("🚀 启动Django后端服务器...")
    os.chdir(Path(__file__).parent)
    
    # 检查数据库迁移
    print("📋 检查数据库迁移...")
    subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
    subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
    
    # 创建超级用户（如果不存在）
    print("👤 检查超级用户...")
    try:
        subprocess.run([sys.executable, 'create_admin.py'], check=True)
    except subprocess.CalledProcessError:
        print("⚠️  超级用户可能已存在")
    
    # 启动Django服务器
    print("🌐 启动Django服务器在端口8002...")
    subprocess.run([sys.executable, 'run_server.py'])

def start_frontend():
    """启动Vue前端"""
    print("🎨 启动Vue前端服务器...")
    frontend_dir = Path(__file__).parent / 'frontend'
    os.chdir(frontend_dir)
    
    # 安装依赖（如果需要）
    if not (frontend_dir / 'node_modules').exists():
        print("📦 安装前端依赖...")
        subprocess.run(['npm', 'install'], check=True)
    
    # 启动Vue开发服务器
    print("🌐 启动Vue开发服务器在端口8085...")
    subprocess.run(['npm', 'run', 'serve'])

def main():
    """主函数"""
    print("🎯 启动Django博客项目...")
    print("=" * 50)
    
    # 在后台线程中启动后端
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # 等待后端启动
    print("⏳ 等待后端启动...")
    time.sleep(5)
    
    # 启动前端
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n👋 项目已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == '__main__':
    main()
