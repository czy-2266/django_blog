import api from './blog';

const apiClient = api;

// 认证相关API
export const authAPI = {
  // 用户登录
  login: async (credentials) => {
    const response = await apiClient.post('/auth/login/', credentials);
    return response;
  },

  // 用户注册
  // userdata:{username,password,email}
  register: async (userData) => {
    const response = await apiClient.post('/auth/register/', userData);
    return response;
  },

  // 获取当前用户信息
  getCurrentUser: async () => {
    const response = await apiClient.get('/auth/users/me/');
    return response;
  },

  // 更新用户信息
  updateUser: async (userData) => {
    const response = await apiClient.put('/auth/users/me/', userData);
    return response;
  },

  // 登出（前端操作）
  logout: () => {
    localStorage.removeItem('token');
    return Promise.resolve();
  }
};