import axios from 'axios'

// 创建axios实例
// 使用相对路径以便在开发和生产环境中都能正常工作
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器 - 添加token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response?.status === 401) {
      // token过期，跳转到登录页
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// 文章相关API
export const articleAPI = {
  // 获取文章列表
  getArticles(params = {}) {
    return api.get('/articles/', { params })
  },

  // 获取文章详情
  getArticle(id) {
    return api.get(`/articles/${id}/`)
  },

  // 创建文章
  createArticle(data) {
    return api.post('/articles/', data)
  },

  // 更新文章
  updateArticle(id, data) {
    return api.put(`/articles/${id}/`, data)
  },

  // 删除文章
  deleteArticle(id) {
    return api.delete(`/articles/${id}/`)
  },

  // 搜索文章
  searchArticles(params) {
    return api.get('/articles/search/', { params })
  }
}

// 分类相关API
export const categoryAPI = {
  // 获取分类列表
  getCategories() {
    return api.get('/categories/')
  },

  // 创建分类
  createCategory(data) {
    return api.post('/categories/', data)
  },

  // 更新分类
  updateCategory(id, data) {
    return api.put(`/categories/${id}/`, data)
  },

  // 删除分类
  deleteCategory(id) {
    return api.delete(`/categories/${id}/`)
  }
}

// 文件上传API
export const uploadAPI = {
  // 上传文件
  uploadFile(file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  // 批量上传文件
  uploadFiles(files) {
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })
    return api.post('/upload/multiple/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  // 上传头像
  uploadAvatar(file) {
    const formData = new FormData()
    formData.append('avatar', file)
    return api.post('/users/me/avatar/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}

// 用户相关API
export const userAPI = {
  // 获取当前用户信息
  getCurrentUser() {
    return api.get('/users/me/')
  },

  // 更新用户信息
  updateProfile(data) {
    return api.put('/users/me/', data)
  }
}

export default api