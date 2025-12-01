<template>
  <div class="blog-home">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <h1 class="welcome-title">
        <el-icon><Star /></el-icon>
        欢迎来到 Ice BLOG
      </h1>
      <p class="welcome-subtitle">分享知识，记录生活，发现美好</p>
    </div>

    <!-- 文章列表 -->
    <div class="articles-section">
      <div class="section-header">
        <h2>
          <el-icon><Document /></el-icon>
          最新文章
        </h2>
        <el-button v-if="authStore.isAuthenticated" type="primary" @click="$router.push('/create')">
          <el-icon><Edit /></el-icon>
          写文章
        </el-button>
        <el-button v-else type="primary" @click="showLoginPrompt">
          <el-icon><Edit /></el-icon>
          写文章
        </el-button>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="3" animated />
      </div>

      <!-- 文章网格 -->
      <div v-else-if="safeArticles.length > 0" class="articles-grid">
        <div
          v-for="article in safeArticles"
          :key="article.id"
          class="article-card"
          @click="goToArticle(article.id)"
        >
          <div class="card-content">
            <h3 class="article-title">{{ article.title }}</h3>
            <p class="article-summary">{{ truncateText(article.summary || article.content, 120) || '暂无摘要...' }}</p>
            <div class="article-meta">
              <span class="category" v-if="article.category">{{ article.category.name }}</span>
              <span class="author">{{ article.author?.username }}</span>
              <span class="time">{{ formatDate(article.created_at) }}</span>
              <span class="views">{{ article.views_count || 0 }} 次阅读</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <el-empty description="还没有文章，来写第一篇吧！">
          <el-button v-if="authStore.isAuthenticated" type="primary" @click="$router.push('/create')">
            开始创作
          </el-button>
          <el-button v-else type="primary" @click="showLoginPrompt">
            开始创作
          </el-button>
        </el-empty>
      </div>
      <!-- 加载更多 -->
      <div v-if="!loading && articles.length > 0 && articles.length < pagination.total" class="load-more">
        <el-button @click="loadMore" :loading="loading" size="large">
          加载更多文章
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { ElMessage, ElMessageBox } from 'element-plus'
import { Star, Document, Edit } from '@element-plus/icons-vue'
import { articleAPI } from '@/api/blog'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'BlogHome',
  components: {
    Star,
    Document,
    Edit
  },
  data() {
    return {
      articles: [],
      loading: true,
      pagination: {
        page: 1,
        size: 10,
        total: 0
      }
    }
  },
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
  computed: {
    safeArticles() {
      return (this.articles || []).filter(a => a && a.id)
    }
  },
  async created() {
    await this.fetchArticles()
  },
  methods: {
    async fetchArticles() {
      try {
        this.loading = true
        console.log('请求文章列表参数：', this.pagination) // 打印请求参数
        const response = await articleAPI.getArticles({
          page: this.pagination.page,
          size: this.pagination.size,
          sort: 'created_at',
          order: 'desc'
        })
        console.log('文章v  列表接口返回成功：', response) // 打印成功响应
        this.articles = response.results || []
        this.pagination.total = response.count || 0
      } catch (error) {
        console.error('获取文章列表失败:', error)
        ElMessage.error('获取文章列表失败，请稍后再试')
        // 如果API调用失败，显示示例数据
        this.articles = [
          {
            id: 1,
            title: '欢迎使用Ice BLOG',
            summary: '最好的明天就是当下，好好生活，为你精彩的人生留下一笔吧！！！',
            content: '欢迎来到Ice BLOG！',
            author: { username: 'Iced Americano' },
            created_at: new Date().toISOString(),
            views_count: 100,
            category: { name: '公告' }
          }
        ]
      } finally {
        this.loading = false
      }
    },
    
    async loadMore() {
      if (this.articles.length >= this.pagination.total) {
        return
      }
      
      try {
        this.pagination.page += 1
        const response = await articleAPI.getArticles({
          page: this.pagination.page,
          size: this.pagination.size,
          sort: 'created_at',
          order: 'desc'
        })
        
        this.articles.push(...(response.items || []))
      } catch (error) {
        console.error('加载更多文章失败:', error)
        ElMessage.error('加载更多文章失败')
        this.pagination.page -= 1 // 回退页码
      }
    },
    
    goToArticle(id) {
      this.$router.push(`/articles/${id}`)
    },
    
    showLoginPrompt() {
      ElMessageBox.confirm(
        '发表文章需要登录，是否前往登录页面？',
        '提示',
        {
          confirmButtonText: '去登录',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        this.$router.push('/login')
      }).catch(() => {
        // 用户取消操作
      })
    },
    
    formatDate(date) {
      if (!date) return ''
      const d = new Date(date)
      return d.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },
    
    truncateText(text, maxLength = 150) {
      if (!text) return ''
      return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
    }
  }
}
</script>

<style scoped>
.blog-home {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  background: linear-gradient(135deg, #B0E0E6 0%, #87CEEB 100%);
  border-radius: 16px;
  padding: 60px 40px;
  text-align: center;
  margin-bottom: 40px;
  color: #2D3748;
}

.welcome-title {
  font-size: 36px;
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(145deg, #4a5568 0%, #2d3748 100%);
  border-radius: 16px;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.section-header h2 {
  margin: 0;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 12px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.section-header h2 .el-icon {
  color: #B0E0E6;
  filter: drop-shadow(0 0 4px rgba(176, 224, 230, 0.5));
}

.section-header .el-button {
  background: linear-gradient(145deg, #B0E0E6 0%, #87CEEB 100%);
  border: 1px solid #B0E0E6;
  color: #2d3748;
  font-weight: 600;
  box-shadow: 
    0 4px 12px rgba(176, 224, 230, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.section-header .el-button:hover {
  background: linear-gradient(145deg, #87CEEB 0%, #B0E0E6 100%);
  box-shadow: 
    0 6px 16px rgba(176, 224, 230, 0.4),
    0 0 0 2px rgba(176, 224, 230, 0.2);
  transform: translateY(-1px);
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.article-card {
  background: linear-gradient(145deg, #4a5568 0%, #2d3748 100%);
  border-radius: 16px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    0 4px 16px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.article-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(145deg, rgba(152, 251, 152, 0.05), rgba(176, 224, 230, 0.05));
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.article-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.4),
    0 10px 30px rgba(0, 0, 0, 0.3),
    0 5px 15px rgba(0, 0, 0, 0.2),
    0 2px 8px rgba(152, 251, 152, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.15),
    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
}

.article-card:hover::before {
  opacity: 1;
}

.article-card:active {
  transform: translateY(-4px) scale(1.01);
  box-shadow: 
    0 12px 40px rgba(0, 0, 0, 0.35),
    0 6px 20px rgba(0, 0, 0, 0.25),
    0 3px 10px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.card-content {
  padding: 24px;
  position: relative;
  z-index: 1;
}

.article-title {
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 12px 0;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.article-summary {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  line-height: 1.6;
  margin: 0 0 16px 0;
}

.article-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 16px;
}

.category {
  background: rgba(152, 251, 152, 0.15);
  color: #98FB98;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  border: 1px solid rgba(152, 251, 152, 0.3);
  backdrop-filter: blur(5px);
}

.load-more {
  text-align: center;
  margin-top: 40px;
  padding: 30px 20px;
  background: linear-gradient(145deg, #4a5568 0%, #2d3748 100%);
  border-radius: 16px;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.load-more .el-button {
  background: linear-gradient(145deg, #98FB98 0%, #90EE90 100%);
  border: 1px solid #98FB98;
  color: #2d3748;
  font-weight: 600;
  font-size: 16px;
  padding: 12px 32px;
  box-shadow: 
    0 4px 12px rgba(152, 251, 152, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.load-more .el-button:hover {
  background: linear-gradient(145deg, #90EE90 0%, #98FB98 100%);
  box-shadow: 
    0 6px 16px rgba(152, 251, 152, 0.4),
    0 0 0 2px rgba(152, 251, 152, 0.2);
  transform: translateY(-2px);
}

.load-more .el-button:disabled {
  background: rgba(45, 55, 72, 0.5);
  color: rgba(255, 255, 255, 0.4);
  border-color: rgba(255, 255, 255, 0.2);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.loading-container {
  padding: 40px 20px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(145deg, #4a5568 0%, #2d3748 100%);
  border-radius: 16px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    0 4px 16px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  margin: 20px 0;
}

.empty-state :deep(.el-empty__description) {
  color: rgba(255, 255, 255, 0.8);
  font-size: 16px;
}

.empty-state :deep(.el-empty__image) {
  opacity: 0.7;
}

@media (max-width: 768px) {
  .welcome-section {
    padding: 40px 20px;
  }
  
  .welcome-title {
    font-size: 28px;
  }
  
  .articles-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .section-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
}
</style>