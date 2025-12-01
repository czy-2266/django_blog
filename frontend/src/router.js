import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from './stores/auth';
import { ElMessage } from 'element-plus';

// 导入组件
import UserLogin from './components/UserLogin.vue';
import UserRegister from './components/UserRegister.vue';
import UserProfile from './components/UserProfile.vue';
// 博客相关组件
import BlogHome from './components/BlogHome.vue';
import ArticleList from './components/ArticleList.vue';
import ArticleEditor from './components/ArticleEditor.vue';
import ArticleDetail from './components/ArticleDetail.vue';
import SearchPage from './components/SearchPage.vue';
import AboutPage from './components/AboutPage.vue';
import ThemeDemo from './components/ThemeDemo.vue';

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/login',
    name: 'Login',
    component: UserLogin,
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register', 
    component: UserRegister,
    meta: { requiresGuest: true }
  },
  {
    path: '/home',
    name: 'Home',
    component: BlogHome
    // 移除 requiresAuth，允许未登录访问
  },
  {
    path: '/articles',
    name: 'ArticleList',
    component: ArticleList
    // 移除 requiresAuth，允许未登录访问
  },
  {
    path: '/articles/:id',
    name: 'ArticleDetail',
    component: ArticleDetail
    // 移除 requiresAuth，允许未登录访问
  },
  {
    path: '/create',
    name: 'ArticleCreate',
    component: ArticleEditor,
    meta: { requiresAuth: true }  // 保持发表文章需要登录
  },
  {
    path: '/articles/edit/:id',
    name: 'ArticleEdit',
    component: ArticleEditor,
    meta: { requiresAuth: true }  // 保持编辑文章需要登录
  },
  {
    path: '/search',
    name: 'Search',
    component: SearchPage
    // 移除 requiresAuth，允许未登录访问
  },
  {
    path: '/about',
    name: 'About',
    component: AboutPage
    // 移除 requiresAuth，允许未登录访问
  },
  {
    path: '/profile',
    name: 'Profile',
    component: UserProfile,
    meta: { requiresAuth: true }  // 保持个人中心需要登录
  },
  {
    path: '/theme-demo',
    name: 'ThemeDemo',
    component: ThemeDemo,
    meta: { requiresAuth: true }  // 保持主题演示需要登录
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 全局路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  
  // 如果有token但没有用户信息，尝试获取用户信息
  if (authStore.token && !authStore.user) {
    await authStore.initAuth();
  }
  
  // 检查是否需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!authStore.isAuthenticated) {
      ElMessage.warning('请先登录');
      next({
        path: '/login',
        query: { redirect: to.fullPath } // 保存重定向地址
      });
    } else {
      next();
    }
  }
  // 检查是否只允许访客访问（仅登录和注册页面）
  else if (to.matched.some(record => record.meta.requiresGuest)) {
    if (authStore.isAuthenticated) {
      next('/home'); // 已登录用户重定向到个人中心
    } else {
      next();
    }
  }
  else {
    next(); // 允许访问不需要认证的页面
  }
});

export default router;