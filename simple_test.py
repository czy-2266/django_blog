#!/usr/bin/env python
"""
简化的API测试脚本
"""
import requests
import json

# API基础URL
BASE_URL = "http://127.0.0.1:8002/api/v1"

def test_register():
    """测试用户注册"""
    print("1️⃣ 测试用户注册...")
    import time
    timestamp = str(int(time.time()))
    register_data = {
        "username": f"testuser{timestamp}",
        "email": f"test{timestamp}@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
        print(f"   注册响应状态: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ 用户注册成功")
            return True
        else:
            print(f"   ❌ 注册失败: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ 注册请求失败: {e}")
        return False

def test_login():
    """测试用户登录"""
    print("\n2️⃣ 测试用户登录...")
    import time
    timestamp = str(int(time.time()))
    login_data = {
        "username": f"testuser{timestamp}",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        print(f"   登录响应状态: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print("   ✅ 用户登录成功")
            print(f"   🔑 Token: {token[:20]}...")
            return token
        else:
            print(f"   ❌ 登录失败: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ 登录请求失败: {e}")
        return None

def test_articles(token):
    """测试文章API"""
    print("\n3️⃣ 测试文章API...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/articles", headers=headers)
        print(f"   文章列表响应状态: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 获取文章列表成功")
            return True
        else:
            print(f"   ❌ 获取文章列表失败: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ 获取文章列表请求失败: {e}")
        return False

def main():
    """主函数"""
    print("🧪 开始测试API接口...")
    print("=" * 50)
    
    # 测试注册
    if not test_register():
        print("❌ 注册失败，停止测试")
        return
    
    # 测试登录
    token = test_login()
    if not token:
        print("❌ 登录失败，停止测试")
        return
    
    # 测试文章API
    test_articles(token)
    
    print("\n" + "=" * 50)
    print("🎉 API接口测试完成！")

if __name__ == "__main__":
    main()