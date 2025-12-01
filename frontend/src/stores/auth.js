import { defineStore } from 'pinia';
import { authAPI } from '../api/auth';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    isLoading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user,
    isLoggedIn: (state) => !!state.token,
  },

  actions: {
    // 登录
    async login(credentials) {
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await authAPI.login(credentials);
        this.token = response.token;  // Django返回的是token字段，不是access_token
        localStorage.setItem('token', this.token);
        
        // 获取用户信息
        await this.fetchCurrentUser();
        
        return { success: true };
      } catch (error) {
        this.error = error.response?.data?.detail || error.response?.data?.error || '登录失败';
        return { success: false, error: this.error };
      } finally {
        this.isLoading = false;
      }
    },

    // 注册
    async register(userData) {
      this.isLoading = true;
      this.error = null;
      
      try {
        // userdata:{username,password,email}
        const response = await authAPI.register(userData);
        return { success: true, data: response };
      } catch (error) {
        console.log(error.response?.data?.detail || '注册失败')
        this.error = error.response?.data?.detail || '注册失败';
        return { success: false, error: this.error };
      } finally {
        this.isLoading = false;
      }
    },

    // 获取当前用户信息
    async fetchCurrentUser() {
      if (!this.token) return;
      
      try {
        this.user = await authAPI.getCurrentUser();
      } catch (error) {
        console.error('获取用户信息失败:', error);
        this.logout();
      }
    },

    // 更新用户信息
    async updateUser(userData) {
      this.isLoading = true;
      this.error = null;
      
      try {
        this.user = await authAPI.updateUser(userData);
        return { success: true };
      } catch (error) {
        this.error = error.response?.data?.detail || '更新失败';
        return { success: false, error: this.error };
      } finally {
        this.isLoading = false;
      }
    },

    // 登出
    logout() {
      authAPI.logout();
      this.user = null;
      this.token = null;
      this.error = null;
    },

    // 清除错误
    clearError() {
      this.error = null;
    },

    // 初始化认证状态
    async initAuth() {
      if (this.token && !this.user) {
        await this.fetchCurrentUser();
      }
    },
  },
});