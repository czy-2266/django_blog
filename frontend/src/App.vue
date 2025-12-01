<template>
  <div id="app">
    <!-- 全局视觉效果组件 -->

    
    <div class="blog-layout">
      <!-- 顶部导航栏 -->
      <header class="blog-header">
        <div class="header-content">
          <div class="logo-section">
            <h1 class="blog-title">
              <el-icon class="logo-icon"><Star /></el-icon>
              Ice BLOG
            </h1>
          </div>
          
          <nav class="main-nav">
            <el-menu
              mode="horizontal"
              class="nav-menu"
              :default-active="$route.path"
              router
              background-color="transparent"
              text-color="#4A5568"
              active-text-color="#87CEEB"
            >
              <el-menu-item index="/home">
                <el-icon><House /></el-icon>
                <span>首页</span>
              </el-menu-item>
              <el-menu-item index="/articles">
                <el-icon><Document /></el-icon>
                <span>文章</span>
              </el-menu-item>
              <el-menu-item index="/create">
                <el-icon><Edit /></el-icon>
                <span>发布文章</span>
              </el-menu-item>
              <el-menu-item index="/about">
                <el-icon><InfoFilled /></el-icon>
                <span>关于</span>
              </el-menu-item>
              <el-menu-item index="/search">
                <el-icon><Search /></el-icon>
                <span>搜索</span>
              </el-menu-item>
              <el-menu-item index="/theme-demo">
                <el-icon><ElPaletteIcon /></el-icon>
                <span>主题</span>
              </el-menu-item>
            </el-menu>
          </nav>

          <!-- 右侧用户区域 -->
          <div class="user-section">
            <div v-if="!authStore.isAuthenticated" class="auth-buttons">
              <el-button type="primary" @click="$router.push('/login')">
                登录
              </el-button>
              <el-button type="success" @click="$router.push('/register')">
                注册
              </el-button>
            </div>

            <div v-else class="user-info">
              <el-dropdown @command="handleUserAction">
                <div class="user-avatar-section">
                  <el-avatar
                    :size="40"
                    :src="authStore.user?.avatar_url"
                    class="user-avatar"
                  >
                    <el-icon><User /></el-icon>
                  </el-avatar>
                  <span class="username">{{ authStore.user?.username }}</span>
                  <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
                </div>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="profile">
                      <el-icon><User /></el-icon>
                      个人资料
                    </el-dropdown-item>
                    <el-dropdown-item command="my-articles">
                      <el-icon><Document /></el-icon>
                      我的文章
                    </el-dropdown-item>
                    <el-dropdown-item command="settings">
                      <el-icon><Setting /></el-icon>
                      设置
                    </el-dropdown-item>
                    <el-dropdown-item divided command="logout">
                      <el-icon><SwitchButton /></el-icon>
                      退出登录
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </div>
      </header>

      <!-- 主内容区域 -->
      <main class="main-content">
        <div class="content-wrapper">
          <router-view v-slot="{ Component }">
            <transition name="page-fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </main>

      <!-- 底部 -->
      <footer class="blog-footer">
        <div class="footer-content">
          <div class="footer-info">
            <h3>
              <el-icon><House /></el-icon>
              Ice BLOG
            </h3>
            <p>一个优雅的个人博客系统</p>
          </div>
          <div class="footer-links">
            <a href="#">关于我们</a>
            <a href="#">联系方式</a>
            <a href="#">隐私政策</a>
          </div>
          <div class="footer-copyright">
            <p>&copy; 2024 Ice BLOG. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from './stores/auth'
import { ElMessage } from 'element-plus'
import {
  Star, House, Document, Edit, InfoFilled, Search,
  User, ArrowDown, Setting, SwitchButton
} from '@element-plus/icons-vue'



export default {
  name: 'App',
  components: {
    Star,
    House,
    Document,
    Edit,
    InfoFilled,
    Search,
    User,
    ArrowDown,
    Setting,
    SwitchButton,
  },
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
  async created() {
    // 初始化认证状态
    await this.authStore.initAuth()
    
    // 如果用户已登录且在登录/注册页，重定向到首页
    if (this.authStore.isAuthenticated && ['/login', '/register'].includes(this.$route.path)) {
      await this.$router.push('/home')
    }
    
    // 移除未登录时的重定向逻辑，允许用户访问主页
  },
  methods: {
    async handleUserAction(command) {
      switch (command) {
        case 'profile':
          await this.$router.push('/profile')
          break
        case 'my-articles':
          await this.$router.push('/my-articles')
          break
        case 'settings':
          await this.$router.push('/settings')
          break
        case 'logout':
          await this.handleLogout()
          break
      }
    },
    async handleLogout() {
      try {
        this.authStore.logout()
        ElMessage.success('退出登录成功')
        await this.$router.push('/home')  // 退出登录后回到首页而不是登录页
      } catch (error) {
        console.error('退出登录失败:', error)
        ElMessage.error('退出登录失败')
      }
    }
  }
}
</script>

<style>
/* Ice BLOG 主题色彩变量 */
:root {
  --ice-primary: #B0E0E6;        /* 浅天蓝色 */
  --ice-primary-light: #E0F6FF;  /* 更浅的天蓝色 */
  --ice-primary-dark: #87CEEB;   /* 稍深的天蓝色 */
  --ice-green: #98FB98;          /* 浅绿色点缀 */
  --ice-green-light: #F0FFF0;    /* 极浅绿色 */
  --ice-green-dark: #90EE90;     /* 稍深浅绿色 */
  --ice-dark: #4A5568;           /* 柔和的深灰色 */
  --ice-dark-light: #718096;     /* 浅一点的灰色 */
  --ice-white: #FFFFFF;          /* 纯白色 */
  --ice-light-gray: #F7FAFC;     /* 浅灰色背景 */
  --ice-border: #E2E8F0;         /* 边框色 */
  --ice-text: #2D3748;           /* 文本色 */
  --ice-text-light: #718096;     /* 浅文本色 */
  --ice-accent: #90CDF4;         /* 强调色 */
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--ice-light-gray) 0%, var(--ice-green-light) 50%, var(--ice-light-gray) 100%);
}

.blog-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* =====  头部样式 ===== */
.blog-header {
  background: linear-gradient(135deg, var(--ice-primary) 0%, var(--ice-green-light) 30%, var(--ice-primary-dark) 100%);
  box-shadow: 0 2px 20px rgba(152, 251, 152, 0.2);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

.logo-section {
  display: flex;
  align-items: center;
}

.blog-title {
  color: var(--ice-dark);
  font-size: 28px;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
  letter-spacing: 1px;
}

.logo-icon {
  font-size: 32px;
  color: var(--ice-dark);
}

/* 导航栏样式 */
.main-nav {
  flex: 1;
  display: flex;
  justify-content: center;
  max-width: 600px;
}

.nav-menu {
  border: none;
  background: transparent;
}

.nav-menu .el-menu-item {
  border: none;
  color: var(--ice-dark);
  font-weight: 500;
  margin: 0 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-menu .el-menu-item:hover {
  background-color: rgba(152, 251, 152, 0.2);
  color: var(--ice-dark);
}

.nav-menu .el-menu-item.is-active {
  background: linear-gradient(135deg, var(--ice-white) 0%, var(--ice-green-light) 100%);
  color: var(--ice-green-dark);
  border: 1px solid var(--ice-green);
}

.nav-menu .el-menu-item span {
  margin-left: 6px;
  font-size: 14px;
}

/* 用户区域样式 */
.user-section {
  display: flex;
  align-items: center;
}

.auth-buttons {
  display: flex;
  gap: 12px;
}

.auth-buttons .el-button {
  border-radius: 20px;
  font-weight: 500;
}

.user-info {
  cursor: pointer;
}

.user-avatar-section {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 25px;
  transition: background-color 0.3s ease;
}

.user-avatar-section:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.user-avatar {
  border: 2px solid var(--ice-dark);
}

.username {
  color: var(--ice-dark);
  font-weight: 500;
  font-size: 14px;
}

.dropdown-icon {
  color: var(--ice-dark);
  font-size: 12px;
}

/* ===== 主内容样式 ===== */
.main-content {
  flex: 1;
  min-height: calc(100vh - 140px);
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
}

/* ===== 底部样式 ===== */
.blog-footer {
  background: linear-gradient(135deg, var(--ice-green-light) 0%, var(--ice-primary-light) 50%, var(--ice-primary) 100%);
  color: var(--ice-dark);
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px 20px;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 40px;
  align-items: start;
}

.footer-info h3 {
  color: var(--ice-dark);
  font-size: 20px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.footer-info p {
  color: var(--ice-dark-light);
  line-height: 1.6;
}

.footer-links {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.footer-links a {
  color: var(--ice-dark-light);
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: var(--ice-dark);
}

.footer-copyright {
  text-align: right;
}

.footer-copyright p {
  color: var(--ice-dark-light);
  font-size: 14px;
}

/* ===== 动画效果 ===== */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* ===== 响应式设计 ===== */
@media (max-width: 1024px) {
  .header-content {
    padding: 0 15px;
  }
  
  .content-wrapper {
    padding: 20px 15px;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    gap: 20px;
    text-align: center;
  }
  
  .footer-copyright {
    text-align: center;
  }
}

@media (max-width: 768px) {
  .header-content {
    height: auto;
    padding: 15px;
    flex-direction: column;
    gap: 15px;
  }
  
  .blog-title {
    font-size: 24px;
  }
  
  .main-nav {
    width: 100%;
    justify-content: center;
  }
  
  .nav-menu {
    justify-content: center;
  }
  
  .nav-menu .el-menu-item {
    margin: 0 4px;
    padding: 0 12px;
  }
  
  .nav-menu .el-menu-item span {
    display: none;
  }
  
  .user-section {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .content-wrapper {
    padding: 15px 10px;
  }
  
  .footer-content {
    padding: 20px 15px;
  }
  
  .blog-title {
    font-size: 20px;
  }
  
  .logo-icon {
    font-size: 24px;
  }
}
</style>