<template>
  <div class="articles-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h1>
          <el-icon><Document /></el-icon>
          文章列表
        </h1>
        <el-button type="primary" @click="$router.push('/create')">
          <el-icon><EditPen /></el-icon>
          写文章
        </el-button>
      </div>
      
      <!-- 筛选和搜索 -->
      <div class="filter-section">
        <div class="filter-left">
          <el-select
            v-model="filters.category_id"
            placeholder="选择分类"
            clearable
            style="width: 150px"
            @change="applyFilters"
          >
            <el-option label="全部分类" :value="null" />
            <el-option
              v-for="category in safeCategories"
              :key="category?.id"
              :label="category?.name"
              :value="category?.id"
            />
          </el-select>
          
          <el-select
            v-model="filters.sort"
            style="width: 120px"
            @change="applyFilters"
          >
            <el-option label="最新发布" value="created_at" />
            <el-option label="最多阅读" value="views_count" />
            <el-option label="最近更新" value="updated_at" />
          </el-select>
        </div>
        
        <div class="filter-right">
          <el-input
            v-model="filters.search"
            placeholder="搜索文章标题和内容..."
            style="width: 300px"
            @keyup.enter="applyFilters"
            @clear="applyFilters"
            clearable
          >
            <template #suffix>
              <el-button @click="applyFilters" type="text">
                <el-icon><Search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </div>
      </div>
    </div>

    <!-- 文章列表 -->
    <div class="articles-container">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="3" animated v-for="i in 3" :key="i" />
      </div>

      <!-- 文章网格 -->
      <div v-else-if="articles.length > 0" class="articles-grid">
        <div
          v-for="article in safeArticles"
          :key="article.id"
          class="article-card"
          @click="goToArticle(article.id)"
        >
          <!-- 文章封面 -->
          <div v-if="article.cover_image" class="article-cover">
            <img :src="article.cover_image" :alt="article.title" />
          </div>
          
          <div class="card-content">
            <!-- 分类标签 -->
            <div v-if="article.category" class="article-category">
              <el-tag size="small" type="primary">{{ article.category.name }}</el-tag>
            </div>
            
            <!-- 文章标题 -->
            <h3 class="article-title">{{ article.title }}</h3>
            
            <!-- 文章摘要 -->
            <p class="article-summary">
              {{ truncateText(article.summary || article.content, 120) }}
            </p>
            
            <!-- 文章标签 -->
            <div v-if="article.tags?.length" class="article-tags">
              <el-tag
                v-for="tag in article.tags.slice(0, 3)"
                :key="tag"
                size="small"
                class="tag-item"
              >
                {{ tag }}
              </el-tag>
              <span v-if="article.tags.length > 3" class="more-tags">
                +{{ article.tags.length - 3 }}
              </span>
            </div>
            
            <!-- 文章元信息 -->
            <div class="article-meta">
              <div class="author-info">
                <el-avatar :size="24" :src="article.author?.avatar_url">
                  {{ article.author?.username?.charAt(0)?.toUpperCase() }}
                </el-avatar>
                <span class="author-name">{{ article.author?.username }}</span>
              </div>
              
              <div class="meta-info">
                <span class="publish-time">{{ formatDate(article.created_at) }}</span>
                <span class="views-count">{{ article.views_count || 0 }} 阅读</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <el-empty 
          :description="filters.search ? '没有找到相关文章' : '还没有文章'"
          :image-size="200"
        >
          <el-button type="primary" @click="$router.push('/create')" v-if="!filters.search">
            写第一篇文章
          </el-button>
          <el-button @click="clearFilters" v-else>
            清除筛选条件
          </el-button>
        </el-empty>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="pagination.total > 0" class="pagination-container">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.size"
        :page-sizes="[12, 24, 48]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="handlePageChange"
        @size-change="handleSizeChange"
      />
    </div>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import {
  Document,
  EditPen,
  Search
} from '@element-plus/icons-vue'
import { articleAPI, categoryAPI } from '@/api/blog'
import { handleCategoriesResponse } from '@/utils/apiHelper'

export default {
  name: 'ArticlesPage',
  components: {
    Document,
    EditPen,
    Search
  },

  data() {
    return {
      articles: [],
      categories: [],
      loading: true,

      // 筛选条件
      filters: {
        search: '',
        category_id: null,
        sort: 'created_at'
      },

      // 分页
      pagination: {
        page: 1,
        size: 12,
        total: 0
      }
    }
  },

  computed: {
    safeArticles() {
      return (this.articles || []).filter(a => a && a.id)
    },
    
    safeCategories() {
      // 确保categories是数组，并过滤掉无效项
      if (!Array.isArray(this.categories)) {
        return []
      }
      return this.categories.filter(c => c != null && c.id)
    }
  },

  async created() {
    // 从URL查询参数中恢复筛选条件
    this.restoreFiltersFromQuery()

    await Promise.all([
      this.loadCategories(),
      this.loadArticles()
    ])
  },

  methods: {
    // 加载文章列表
    async loadArticles(showLoading = true) {
      try {
        if (showLoading) this.loading = true

        const params = {
          page: this.pagination.page,
          size: this.pagination.size,
          sort: this.filters.sort,
          order: 'desc'
        }

        // 添加筛选条件
        if (this.filters.search) {
          params.search = this.filters.search
        }
        if (this.filters.category_id) {
          params.category_id = this.filters.category_id
        }
        console.log('请求文章列表参数：', this.pagination) // 打印请求参数
        const response = await articleAPI.getArticles({
          page: this.pagination.page,
          size: this.pagination.size,
          sort: 'created_at',
          order: 'desc'
        })
        console.log('文章列表接口返回成功：', response) // 打印成功响应

        this.articles = response.results || []
        this.pagination.total = response.count || 0

        // 更新URL查询参数
        this.updateQueryParams()
      } catch (error) {
        console.error('加载文章列表失败:', error)
        ElMessage.error('加载文章列表失败，请稍后重试')

        // 显示示例数据
        this.articles = [
          {
            id: 1,
            title: '欢迎使用Ice BLOG',
            summary: '加油！陌生人！',
            content: '欢迎来到Ice BLOG！',
            author: { username: 'admin', avatar_url: null },
            created_at: new Date().toISOString(),
            views_count: 100,
            category: { name: '公告' },
            tags: ['欢迎', '公告']
          }
        ]
        this.pagination.total = 1
      } finally {
        this.loading = false
      }
    },

    // 加载分类列表
    async loadCategories() {
      try {
        const response = await categoryAPI.getCategories()
        this.categories = handleCategoriesResponse(response)
      } catch (error) {
        console.error('加载分类失败:', error)
        this.categories = []
      }
    },

    // 应用筛选条件
    async applyFilters() {
      this.pagination.page = 1 // 重置到第一页
      await this.loadArticles()
    },

    // 清除筛选条件
    async clearFilters() {
      this.filters = {
        search: '',
        category_id: null,
        sort: 'created_at'
      }
      await this.applyFilters()
    },

    // 页码变化
    async handlePageChange(page) {
      this.pagination.page = page
      await this.loadArticles()

      // 滚动到顶部
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },

    // 页面大小变化
    async handleSizeChange(size) {
      this.pagination.size = size
      this.pagination.page = 1
      await this.loadArticles()
    },

    // 跳转到文章详情
    goToArticle(id) {
      this.$router.push(`/articles/${id}`)
    },

    // 文本截断
    truncateText(text, maxLength = 120) {
      if (!text) return ''
      return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
    },

    // 格式化日期
    formatDate(date) {
      if (!date) return ''
      const d = new Date(date)
      const now = new Date()
      const diff = now - d

      // 小于1天显示相对时间
      if (diff < 24 * 60 * 60 * 1000) {
        if (diff < 60 * 60 * 1000) {
          const minutes = Math.floor(diff / (60 * 1000))
          return minutes < 1 ? '刚刚' : `${minutes}分钟前`
        } else {
          const hours = Math.floor(diff / (60 * 60 * 1000))
          return `${hours}小时前`
        }
      }

      // 大于1天显示具体日期
      return d.toLocaleDateString('zh-CN', {
        month: 'short',
        day: 'numeric'
      })
    },

    // 从URL查询参数恢复筛选条件
    restoreFiltersFromQuery() {
      const query = this.$route.query

      if (query.search) this.filters.search = query.search
      if (query.category_id) this.filters.category_id = Number(query.category_id)
      if (query.sort) this.filters.sort = query.sort
      if (query.page) this.pagination.page = Number(query.page)
      if (query.size) this.pagination.size = Number(query.size)
    },

    // 更新URL查询参数
    updateQueryParams() {
      const query = {}

      if (this.filters.search) query.search = this.filters.search
      if (this.filters.category_id) query.category_id = this.filters.category_id
      if (this.filters.sort !== 'created_at') query.sort = this.filters.sort
      if (this.pagination.page > 1) query.page = this.pagination.page
      if (this.pagination.size !== 12) query.size = this.pagination.size

      // 只在查询参数发生变化时更新URL
      if (JSON.stringify(query) !== JSON.stringify(this.$route.query)) {
        this.$router.replace({ query })
      }
    }
  },

  watch: {
    '$route.query'() {
      // 监听查询参数变化（如浏览器前进后退）
      this.restoreFiltersFromQuery()
      this.loadArticles()
    }
  }
}
</script>


<style scoped>
.articles-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 30px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px;
  background: linear-gradient(145deg, #4a5568 0%, #2d3748 100%);
  border-radius: 16px;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.header-content h1 {
  margin: 0;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 12px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.header-content h1 .el-icon {
  color: #98FB98;
  filter: drop-shadow(0 0 4px rgba(152, 251, 152, 0.5));
}

.header-content .el-button {
  background: linear-gradient(145deg, #98FB98 0%, #90EE90 100%);
  border: 1px solid #98FB98;
  color: #2d3748;
  font-weight: 600;
  box-shadow: 
    0 4px 12px rgba(152, 251, 152, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.header-content .el-button:hover {
  background: linear-gradient(145deg, #90EE90 0%, #98FB98 100%);
  box-shadow: 
    0 6px 16px rgba(152, 251, 152, 0.4),
    0 0 0 2px rgba(152, 251, 152, 0.2);
  transform: translateY(-1px);
}

.filter-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(145deg, #4a5568 0%, #2d3748 100%);
  padding: 20px;
  border-radius: 16px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    0 4px 16px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.filter-left {
  display: flex;
  gap: 16px;
  align-items: center;
}

/* 深色主题输入框样式 */
:deep(.el-select) {
  --el-select-input-color: #ffffff;
  --el-select-placeholder-color: rgba(255, 255, 255, 0.6);
}

:deep(.el-select .el-input__wrapper) {
  background: linear-gradient(145deg, #2d3748 0%, #1a202c 100%);
  border: 1px solid rgba(152, 251, 152, 0.3);
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  transition: all 0.3s ease;
}

:deep(.el-select .el-input__wrapper:hover) {
  border-color: rgba(152, 251, 152, 0.5);
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.3),
    0 0 0 2px rgba(152, 251, 152, 0.1);
}

:deep(.el-select .el-input__wrapper.is-focus) {
  border-color: #98FB98;
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.3),
    0 0 0 2px rgba(152, 251, 152, 0.2);
}

:deep(.el-input) {
  --el-input-text-color: #ffffff;
  --el-input-placeholder-color: rgba(255, 255, 255, 0.6);
}

:deep(.el-input__wrapper) {
  background: linear-gradient(145deg, #2d3748 0%, #1a202c 100%);
  border: 1px solid rgba(176, 224, 230, 0.3);
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  border-color: rgba(176, 224, 230, 0.5);
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.3),
    0 0 0 2px rgba(176, 224, 230, 0.1);
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #B0E0E6;
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.3),
    0 0 0 2px rgba(176, 224, 230, 0.2);
}

/* 下拉菜单样式 */
:deep(.el-select-dropdown) {
  background: linear-gradient(145deg, #2d3748 0%, #1a202c 100%);
  border: 1px solid rgba(152, 251, 152, 0.3);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 4px 16px rgba(0, 0, 0, 0.3);
}

:deep(.el-select-dropdown .el-select-dropdown__item) {
  color: rgba(255, 255, 255, 0.9);
  background: transparent;
}

:deep(.el-select-dropdown .el-select-dropdown__item:hover) {
  background: rgba(152, 251, 152, 0.1);
  color: #98FB98;
}

:deep(.el-select-dropdown .el-select-dropdown__item.selected) {
  background: rgba(152, 251, 152, 0.2);
  color: #98FB98;
}

.articles-container {
  margin-bottom: 40px;
}

.loading-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
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
  overflow: hidden;
  position: relative;
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

.article-cover {
  width: 100%;
  height: 180px;
  overflow: hidden;
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.article-card:hover .article-cover img {
  transform: scale(1.05);
}

.card-content {
  padding: 24px;
  position: relative;
  z-index: 1;
}

.article-category {
  margin-bottom: 12px;
}

.article-category .el-tag {
  background: rgba(152, 251, 152, 0.15);
  color: #98FB98;
  border: 1px solid rgba(152, 251, 152, 0.3);
  backdrop-filter: blur(10px);
}

.article-title {
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 12px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.article-summary {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  line-height: 1.6;
  margin: 0 0 16px 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
  align-items: center;
}

.tag-item {
  background: rgba(176, 224, 230, 0.15);
  color: #B0E0E6;
  border: 1px solid rgba(176, 224, 230, 0.3);
  backdrop-filter: blur(5px);
}

.more-tags {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.author-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.author-name {
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
}

.meta-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
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

.pagination-container {
  display: flex;
  justify-content: center;
  padding: 40px 20px;
}

/* 分页组件深色主题样式 */
:deep(.el-pagination) {
  --el-pagination-font-size: 14px;
  --el-pagination-bg-color: #2d3748;
  --el-pagination-text-color: #ffffff;
  --el-pagination-border-radius: 8px;
  --el-pagination-button-color: rgba(255, 255, 255, 0.8);
  --el-pagination-button-bg-color: linear-gradient(145deg, #4a5568 0%, #2d3748 100%);
  --el-pagination-button-disabled-color: rgba(255, 255, 255, 0.3);
  --el-pagination-button-disabled-bg-color: rgba(45, 55, 72, 0.5);
  --el-pagination-hover-color: #98FB98;
  background: transparent;
}

:deep(.el-pagination .el-pager li) {
  background: linear-gradient(145deg, #4a5568 0%, #2d3748 100%);
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(152, 251, 152, 0.3);
  border-radius: 8px;
  margin: 0 4px;
  font-weight: 500;
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

:deep(.el-pagination .el-pager li:hover) {
  background: linear-gradient(145deg, #98FB98 0%, #90EE90 100%);
  color: #2d3748;
  border-color: #98FB98;
  box-shadow: 
    0 4px 12px rgba(152, 251, 152, 0.3),
    0 0 0 2px rgba(152, 251, 152, 0.1);
  transform: translateY(-1px);
}

:deep(.el-pagination .el-pager li.is-active) {
  background: linear-gradient(145deg, #98FB98 0%, #90EE90 100%);
  color: #2d3748;
  border-color: #98FB98;
  font-weight: 600;
  box-shadow: 
    0 4px 12px rgba(152, 251, 152, 0.4),
    0 0 0 2px rgba(152, 251, 152, 0.2);
}

:deep(.el-pagination .btn-prev),
:deep(.el-pagination .btn-next) {
  background: linear-gradient(145deg, #4a5568 0%, #2d3748 100%);
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(176, 224, 230, 0.3);
  border-radius: 8px;
  font-weight: 500;
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

:deep(.el-pagination .btn-prev:hover),
:deep(.el-pagination .btn-next:hover) {
  background: linear-gradient(145deg, #B0E0E6 0%, #87CEEB 100%);
  color: #2d3748;
  border-color: #B0E0E6;
  box-shadow: 
    0 4px 12px rgba(176, 224, 230, 0.3),
    0 0 0 2px rgba(176, 224, 230, 0.1);
  transform: translateY(-1px);
}

:deep(.el-pagination .btn-prev:disabled),
:deep(.el-pagination .btn-next:disabled) {
  background: rgba(45, 55, 72, 0.5);
  color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.1);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

:deep(.el-pagination .el-pagination__total),
:deep(.el-pagination .el-pagination__jump) {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

:deep(.el-pagination .el-select .el-input__wrapper) {
  background: linear-gradient(145deg, #2d3748 0%, #1a202c 100%);
  border: 1px solid rgba(176, 224, 230, 0.3);
  border-radius: 6px;
}

:deep(.el-pagination .el-input__wrapper input) {
  color: #ffffff;
  text-align: center;
  font-weight: 500;
}

@media (max-width: 768px) {
  .articles-page {
    margin: 12px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .filter-section {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .filter-left {
    flex-direction: column;
    gap: 12px;
  }
  
  .filter-right {
    width: 100%;
  }
  
  .filter-right .el-input {
    width: 100% !important;
  }
  
  .articles-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .article-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .meta-info {
    align-items: flex-start;
  }
}
</style>