<template>
  <div class="search-page">
    <!-- 搜索头部 -->
    <div class="search-header">
      <h1>
        <el-icon><Search /></el-icon>
        文章搜索
      </h1>
      <p class="search-subtitle">发现更多有趣的内容</p>
    </div>

    <!-- 搜索框区域 -->
    <div class="search-container">
      <div class="search-box">
        <el-input
          v-model="searchQuery"
          size="large"
          placeholder="搜索文章标题、内容、标签..."
          class="search-input"
          @keyup.enter="performSearch"
          @clear="clearSearch"
          clearable
        >
          <template #suffix>
            <el-button @click="performSearch" type="text" :loading="searching">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
        
        <el-button
          type="primary"
          size="large"
          @click="performSearch"
          :loading="searching"
          class="search-button"
        >
          搜索
        </el-button>
      </div>

      <!-- 高级搜索选项 -->
      <div class="advanced-search" v-show="showAdvanced">
        <el-form :model="filters" inline class="search-filters">
          <el-form-item label="分类">
            <el-select
              v-model="filters.category_id"
              placeholder="选择分类"
              clearable
              style="width: 150px"
            >
              <el-option
                v-for="category in safeCategories"
                :key="category?.id"
                :label="category?.name"
                :value="category?.id"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="作者">
            <el-input
              v-model="filters.author"
              placeholder="输入作者名"
              style="width: 150px"
              clearable
            />
          </el-form-item>

          <el-form-item label="时间范围">
            <el-date-picker
              v-model="filters.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              style="width: 220px"
            />
          </el-form-item>

          <el-form-item label="排序">
            <el-select v-model="filters.sort" style="width: 120px">
              <el-option label="相关度" value="relevance" />
              <el-option label="最新发布" value="created_at" />
              <el-option label="最多阅读" value="views_count" />
            </el-select>
          </el-form-item>
        </el-form>
      </div>

      <!-- 切换高级搜索 -->
      <div class="search-toggle">
        <el-button @click="showAdvanced = !showAdvanced" text type="primary">
          <el-icon><Setting /></el-icon>
          {{ showAdvanced ? '收起' : '高级搜索' }}
        </el-button>
      </div>
    </div>

    <!-- 搜索历史 -->
    <div v-if="!hasSearched && searchHistory.length" class="search-history">
      <div class="history-header">
        <h3>搜索历史</h3>
        <el-button @click="clearHistory" text type="danger" size="small">
          <el-icon><Delete /></el-icon>
          清空
        </el-button>
      </div>
      <div class="history-tags">
        <el-tag
          v-for="(item, index) in searchHistory"
          :key="index"
          @click="useHistorySearch(item)"
          closable
          @close="removeHistoryItem(index)"
          class="history-tag"
        >
          {{ item }}
        </el-tag>
      </div>
    </div>

    <!-- 热门搜索 -->
    <div v-if="!hasSearched" class="popular-searches">
      <h3>热门搜索</h3>
      <div class="popular-tags">
        <el-tag
          v-for="tag in popularSearches"
          :key="tag"
          @click="usePopularSearch(tag)"
          class="popular-tag"
        >
          {{ tag }}
        </el-tag>
      </div>
    </div>

    <!-- 搜索结果 -->
    <div v-if="hasSearched" class="search-results">
      <div class="results-header">
        <h3>
          搜索结果
          <span v-if="searchResults.total > 0" class="result-count">
            （共找到 {{ searchResults.total }} 条结果）
          </span>
        </h3>
        
        <div class="result-stats">
          <span class="search-time">搜索耗时：{{ searchTime }}ms</span>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="searching" class="loading-container">
        <el-skeleton :rows="3" animated v-for="i in 3" :key="i" />
      </div>

      <!-- 搜索结果列表 -->
      <div v-else-if="searchResults.items?.length" class="results-list">
        <div
          v-for="article in searchResults.items"
          :key="article.id"
          class="result-item"
          @click="goToArticle(article.id)"
        >
          <div class="result-content">
            <h4 class="result-title" v-html="highlightKeywords(article.title)"></h4>
            <p class="result-summary" v-html="highlightKeywords(article.summary || article.content)"></p>
            
            <div class="result-meta">
              <span class="result-category" v-if="article.category">
                {{ article.category.name }}
              </span>
              <span class="result-author">{{ article.author?.username }}</span>
              <span class="result-date">{{ formatDate(article.created_at) }}</span>
              <span class="result-views">{{ article.views_count || 0 }} 阅读</span>
            </div>
            
            <!-- 匹配的标签 -->
            <div v-if="article.tags?.length" class="result-tags">
              <el-tag
                v-for="tag in article.tags"
                :key="tag"
                size="small"
                class="result-tag"
              >
                {{ tag }}
              </el-tag>
            </div>
          </div>
        </div>
      </div>

      <!-- 空搜索结果 -->
      <div v-else class="empty-results">
        <el-empty
          description="没有找到相关文章"
          :image-size="150"
        >
          <template #description>
            <p>没有找到与 "<strong>{{ searchQuery }}</strong>" 相关的文章</p>
            <p>建议：</p>
            <ul>
              <li>检查关键词拼写是否正确</li>
              <li>尝试使用更通用的关键词</li>
              <li>使用空格分隔多个关键词</li>
            </ul>
          </template>
          <el-button type="primary" @click="clearSearch">
            重新搜索
          </el-button>
        </el-empty>
      </div>

      <!-- 搜索分页 -->
      <div v-if="searchResults.total > 0" class="search-pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50]"
          :total="searchResults.total"
          layout="total, sizes, prev, pager, next"
          @current-change="handlePageChange"
          @size-change="handleSizeChange"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import {
  Search,
  Setting,
  Delete
} from '@element-plus/icons-vue'
import { articleAPI, categoryAPI } from '@/api/blog'

export default {
  name: 'SearchPage',
  components: {
    Search,
    Setting,
    Delete
  },
  
  data() {
    return {
      searchQuery: '',
      searching: false,
      hasSearched: false,
      searchTime: 0,
      showAdvanced: false,
      
      // 搜索筛选条件
      filters: {
        category_id: null,
        author: '',
        dateRange: null,
        sort: 'relevance'
      },
      
      // 搜索结果
      searchResults: {
        items: [],
        total: 0
      },
      
      // 分页
      pagination: {
        page: 1,
        size: 10
      },
      
      // 分类列表
      categories: [],
      
      // 搜索历史（本地存储）
      searchHistory: [],
      
      // 热门搜索词
      popularSearches: [
        'Vue.js',
        'JavaScript',
        'Python',
        '前端开发',
        '后端开发',
        '数据库',
        '算法',
        '机器学习'
      ]
    }
  },
  
  computed: {
    safeCategories() {
      return (this.categories || []).filter(c => c != null)
    }
  },
  
  async created() {
    await this.loadCategories()
    this.loadSearchHistory()
    
    // 从URL恢复搜索查询
    const query = this.$route.query.q
    if (query) {
      this.searchQuery = query
      await this.performSearch(false)
    }
  },
  
  methods: {
    // 加载分类列表
    async loadCategories() {
      try {
        const response = await categoryAPI.getCategories()
        // 处理Django REST Framework的分页响应格式
        this.categories = Array.isArray(response) ? response : (response.results || [])
      } catch (error) {
        console.error('加载分类失败:', error)
        this.categories = []
      }
    },
    
    // 执行搜索
    async performSearch(addToHistory = true) {
      if (!this.searchQuery.trim()) {
        ElMessage.warning('请输入搜索关键词')
        return
      }
      
      try {
        this.searching = true
        const startTime = Date.now()
        
        const params = {
          q: this.searchQuery.trim(),
          page: this.pagination.page,
          size: this.pagination.size,
          sort: this.filters.sort
        }
        
        // 添加筛选条件
        if (this.filters.category_id) {
          params.category_id = this.filters.category_id
        }
        if (this.filters.author) {
          params.author = this.filters.author
        }
        if (this.filters.dateRange?.length === 2) {
          params.start_date = this.filters.dateRange[0].toISOString().split('T')[0]
          params.end_date = this.filters.dateRange[1].toISOString().split('T')[0]
        }
        
        const response = await articleAPI.searchArticles(params)
        
        this.searchResults = {
          items: response.items || [],
          total: response.total || 0
        }
        
        this.searchTime = Date.now() - startTime
        this.hasSearched = true
        
        // 添加到搜索历史
        if (addToHistory) {
          this.addToHistory(this.searchQuery)
        }
        
        // 更新URL
        this.updateURL()
        
      } catch (error) {
        console.error('搜索失败:', error)
        ElMessage.error('搜索失败，请稍后重试')
        
        // 显示示例搜索结果
        this.searchResults = {
          items: [
            {
              id: 1,
              title: '包含搜索关键词的示例文章',
              summary: `这是一个包含"${this.searchQuery}"关键词的示例文章摘要...`,
              content: '文章内容',
              author: { username: 'admin' },
              created_at: new Date().toISOString(),
              views_count: 100,
              category: { name: '示例分类' },
              tags: ['示例', '搜索']
            }
          ],
          total: 1
        }
        this.searchTime = 50
        this.hasSearched = true
        
      } finally {
        this.searching = false
      }
    },
    
    // 清除搜索
    clearSearch() {
      this.searchQuery = ''
      this.hasSearched = false
      this.searchResults = { items: [], total: 0 }
      this.pagination.page = 1
      this.resetFilters()
      
      // 清除URL参数
      this.$router.replace({ query: {} })
    },
    
    // 重置筛选条件
    resetFilters() {
      this.filters = {
        category_id: null,
        author: '',
        dateRange: null,
        sort: 'relevance'
      }
    },
    
    // 页码变化
    async handlePageChange(page) {
      this.pagination.page = page
      await this.performSearch(false)
      
      // 滚动到搜索结果顶部
      const resultsEl = this.$el.querySelector('.search-results')
      if (resultsEl) {
        resultsEl.scrollIntoView({ behavior: 'smooth' })
      }
    },
    
    // 页面大小变化
    async handleSizeChange(size) {
      this.pagination.size = size
      this.pagination.page = 1
      await this.performSearch(false)
    },
    
    // 跳转到文章
    goToArticle(id) {
      this.$router.push(`/articles/${id}`)
    },
    
    // 高亮关键词
    highlightKeywords(text) {
      if (!text || !this.searchQuery) return text
      
      const keywords = this.searchQuery.split(/\s+/).filter(k => k)
      let highlightedText = text
      
      keywords.forEach(keyword => {
        const regex = new RegExp(`(${keyword})`, 'gi')
        highlightedText = highlightedText.replace(regex, '<mark>$1</mark>')
      })
      
      return highlightedText
    },
    
    // 搜索历史管理
    loadSearchHistory() {
      try {
        const history = localStorage.getItem('search_history')
        this.searchHistory = history ? JSON.parse(history) : []
      } catch (error) {
        this.searchHistory = []
      }
    },
    
    addToHistory(query) {
      const trimmedQuery = query.trim()
      if (!trimmedQuery) return
      
      // 移除重复项并添加到开头
      this.searchHistory = [
        trimmedQuery,
        ...this.searchHistory.filter(item => item !== trimmedQuery)
      ].slice(0, 10) // 最多保存10条历史
      
      // 保存到本地存储
      try {
        localStorage.setItem('search_history', JSON.stringify(this.searchHistory))
      } catch (error) {
        console.error('保存搜索历史失败:', error)
      }
    },
    
    removeHistoryItem(index) {
      this.searchHistory.splice(index, 1)
      try {
        localStorage.setItem('search_history', JSON.stringify(this.searchHistory))
      } catch (error) {
        console.error('更新搜索历史失败:', error)
      }
    },
    
    clearHistory() {
      this.searchHistory = []
      try {
        localStorage.removeItem('search_history')
      } catch (error) {
        console.error('清除搜索历史失败:', error)
      }
      ElMessage.success('搜索历史已清空')
    },
    
    // 使用历史搜索
    async useHistorySearch(query) {
      this.searchQuery = query
      await this.performSearch()
    },
    
    // 使用热门搜索
    async usePopularSearch(tag) {
      this.searchQuery = tag
      await this.performSearch()
    },
    
    // 格式化日期
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('zh-CN')
    },
    
    // 更新URL
    updateURL() {
      const query = {}
      if (this.searchQuery) query.q = this.searchQuery
      if (this.pagination.page > 1) query.page = this.pagination.page
      
      this.$router.replace({ query })
    }
  }
}
</script>

<style scoped>
.search-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.search-header {
  text-align: center;
  margin-bottom: 40px;
}

.search-header h1 {
  margin: 0 0 12px 0;
  color: #2c3e50;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.search-subtitle {
  color: #718096;
  margin: 0;
}

.search-container {
  background: white;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 30px;
}

.search-box {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
}

.search-button {
  min-width: 100px;
}

.advanced-search {
  border-top: 1px solid #f0f0f0;
  padding-top: 20px;
  margin-top: 20px;
}

.search-filters :deep(.el-form-item) {
  margin-bottom: 16px;
}

.search-toggle {
  text-align: center;
}

.search-history,
.popular-searches {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  margin-bottom: 24px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.history-header h3,
.popular-searches h3 {
  margin: 0 0 16px 0;
  color: #516172;
}

.history-tags,
.popular-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.history-tag,
.popular-tag {
  cursor: pointer;
  transition: all 0.2s;
}

.history-tag:hover,
.popular-tag:hover {
  background: #87CEEB;
  color: white;
}

.search-results {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.results-header h3 {
  margin: 0;
  color: #2c3e50;
}

.result-count {
  color: #718096;
  font-weight: normal;
  font-size: 14px;
}

.search-time {
  color: #adb5bd;
  font-size: 12px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.result-item {
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.result-item:hover {
  border-color: #87CEEB;
  box-shadow: 0 2px 8px rgba(135, 206, 235, 0.2);
}

.result-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.result-title :deep(mark) {
  background: #87CEEB;
  color: white;
  padding: 2px 4px;
  border-radius: 3px;
}

.result-summary {
  color: #718096;
  line-height: 1.6;
  margin: 0 0 16px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.result-summary :deep(mark) {
  background: #fff3cd;
  color: #856404;
  padding: 1px 3px;
  border-radius: 2px;
}

.result-meta {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #adb5bd;
  margin-bottom: 12px;
}

.result-category {
  background: #87CEEB;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.result-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.result-tag {
  background: #f8f9fa;
  color: #6c757d;
  border-color: #e9ecef;
}

.empty-results {
  text-align: center;
  padding: 40px 20px;
}

.empty-results ul {
  text-align: left;
  display: inline-block;
  color: #718096;
  font-size: 14px;
}

.search-pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
  padding: 30px 20px;
  background: linear-gradient(145deg, #4a5568 0%, #2d3748 100%);
  border-radius: 16px;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

/* 搜索页分页组件深色主题样式 */
.search-pagination :deep(.el-pagination) {
  --el-pagination-font-size: 14px;
  --el-pagination-bg-color: #2d3748;
  --el-pagination-text-color: #ffffff;
  --el-pagination-border-radius: 8px;
  --el-pagination-button-color: rgba(255, 255, 255, 0.8);
  --el-pagination-button-bg-color: linear-gradient(145deg, #4a5568 0%, #2d3748 100%);
  --el-pagination-button-disabled-color: rgba(255, 255, 255, 0.3);
  --el-pagination-button-disabled-bg-color: rgba(45, 55, 72, 0.5);
  --el-pagination-hover-color: #B0E0E6;
  background: transparent;
}

.search-pagination :deep(.el-pagination .el-pager li) {
  background: linear-gradient(145deg, #4a5568 0%, #2d3748 100%);
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(176, 224, 230, 0.3);
  border-radius: 8px;
  margin: 0 4px;
  font-weight: 500;
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.search-pagination :deep(.el-pagination .el-pager li:hover) {
  background: linear-gradient(145deg, #B0E0E6 0%, #87CEEB 100%);
  color: #2d3748;
  border-color: #B0E0E6;
  box-shadow: 
    0 4px 12px rgba(176, 224, 230, 0.3),
    0 0 0 2px rgba(176, 224, 230, 0.1);
  transform: translateY(-1px);
}

.search-pagination :deep(.el-pagination .el-pager li.is-active) {
  background: linear-gradient(145deg, #B0E0E6 0%, #87CEEB 100%);
  color: #2d3748;
  border-color: #B0E0E6;
  font-weight: 600;
  box-shadow: 
    0 4px 12px rgba(176, 224, 230, 0.4),
    0 0 0 2px rgba(176, 224, 230, 0.2);
}

.search-pagination :deep(.el-pagination .btn-prev),
.search-pagination :deep(.el-pagination .btn-next) {
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

.search-pagination :deep(.el-pagination .btn-prev:hover),
.search-pagination :deep(.el-pagination .btn-next:hover) {
  background: linear-gradient(145deg, #B0E0E6 0%, #87CEEB 100%);
  color: #2d3748;
  border-color: #B0E0E6;
  box-shadow: 
    0 4px 12px rgba(176, 224, 230, 0.3),
    0 0 0 2px rgba(176, 224, 230, 0.1);
  transform: translateY(-1px);
}

.search-pagination :deep(.el-pagination .el-pagination__total),
.search-pagination :deep(.el-pagination .el-pagination__sizes) {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

@media (max-width: 768px) {
  .search-page {
    padding: 12px;
  }
  
  .search-container {
    padding: 20px;
  }
  
  .search-box {
    flex-direction: column;
  }
  
  .results-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .result-meta {
    flex-direction: column;
    gap: 8px;
  }
  
  .history-tags,
  .popular-tags {
    gap: 8px;
  }
}
</style>