<template>
  <div class="article-detail">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>

    <!-- 文章内容 -->
    <div v-else-if="article" class="article-container">
      <!-- 文章头部 -->
      <div class="article-header">
        <div class="breadcrumb">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item :to="{ path: '/articles' }">文章</el-breadcrumb-item>
            <el-breadcrumb-item v-if="article.category">{{ article.category.name }}</el-breadcrumb-item>
            <el-breadcrumb-item>{{ article.title }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <h1 class="article-title">{{ article.title }}</h1>
        
        <div class="article-meta">
          <div class="meta-info">
            <el-avatar :size="40" :src="article.author?.avatar_url" class="author-avatar">
              <span>{{ article.author?.username?.charAt(0)?.toUpperCase() }}</span>
            </el-avatar>
            <div class="author-info">
              <div class="author-name">{{ article.author?.username }}</div>
              <div class="publish-info">
                <span class="publish-time">{{ formatDate(article.created_at) }}</span>
                <span class="separator">•</span>
                <span class="views-count">{{ article.views_count || 0 }} 次阅读</span>
                <span v-if="article.updated_at !== article.created_at" class="separator">•</span>
                <span v-if="article.updated_at !== article.created_at" class="update-time">
                  更新于 {{ formatDate(article.updated_at) }}
                </span>
              </div>
            </div>
          </div>

          <!-- 文章操作 -->
          <div v-if="canEdit" class="article-actions">
            <el-button @click="editArticle" type="primary" size="small">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button @click="deleteArticle" type="danger" size="small">
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </div>
        </div>

        <!-- 文章标签和分类 -->
        <div class="article-tags" v-if="article.tags?.length || article.category">
          <el-tag v-if="article.category" type="primary" class="category-tag">
            {{ article.category.name }}
          </el-tag>
          <el-tag
            v-for="tag in article.tags"
            :key="tag"
            class="tag-item"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>

      <!-- 文章摘要 -->
      <div v-if="article.summary" class="article-summary">
        {{ article.summary }}
      </div>

      <!-- 文章正文 -->
      <div class="article-content" v-html="renderedContent"></div>

      <!-- 文章底部 -->
      <div class="article-footer">
        <div class="article-stats">
          <div class="stat-item">
            <el-icon><View /></el-icon>
            <span>{{ article.views_count || 0 }} 次阅读</span>
          </div>
          <div class="stat-item">
            <el-icon><Calendar /></el-icon>
            <span>发布于 {{ formatDate(article.created_at) }}</span>
          </div>
        </div>

        <!-- 分享按钮 -->
        <div class="share-buttons">
          <el-button @click="shareArticle" size="small">
            <el-icon><Share /></el-icon>
            分享文章
          </el-button>
        </div>
      </div>
    </div>

    <!-- 错误状态 -->
    <div v-else class="error-container">
      <el-result
        icon="error"
        title="文章加载失败"
        sub-title="抱歉，无法找到此文章或文章已被删除"
      >
        <template #extra>
          <el-button type="primary" @click="$router.push('/articles')">
            返回文章列表
          </el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<script>
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Edit,
  Delete,
  View,
  Calendar,
  Share
} from '@element-plus/icons-vue'
import { articleAPI } from '@/api/blog'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'ArticleDetail',
  components: {
    Edit,
    Delete,
    View,
    Calendar,
    Share
  },
  
  data() {
    return {
      article: null,
      loading: true
    }
  },
  methods: {
    async loadArticle() {
      try {
        this.loading = true
        const response = await articleAPI.getArticle(this.articleId)
        console.log('文章详情数据:', response)
        this.article=response

      } catch (error) {
        console.error('加载文章失败:', error)
        if (error.response?.status === 404) {
          ElMessage.error('文章不存在')
        } else {
          ElMessage.error('加载文章失败，请稍后重试')
        }
        this.article = null
      } finally {
        this.loading = false
      }
    },

    editArticle() {
      this.$router.push(`/articles/edit/${this.articleId}`)
    },

    async deleteArticle() {
      try {
        await ElMessageBox.confirm(
          '确定要删除这篇文章吗？删除后无法恢复！',
          '确认删除',
          {
            confirmButtonText: '删除',
            cancelButtonText: '取消',
            type: 'error'
          }
        )

        await articleAPI.deleteArticle(this.articleId)
        ElMessage.success('文章删除成功')
        this.$router.push('/articles')
      } catch (error) {
        if (error === 'cancel') return
        console.error('删除文章失败:', error)
        ElMessage.error('删除文章失败，请重试')
      }
    },

    shareArticle() {
      const url = window.location.href
      const title = this.article.title

      if (navigator.share) {
        navigator.share({
          title: title,
          url: url
        }).catch(err => {
          console.log('分享失败:', err)
          this.copyToClipboard(url)
        })
      } else {
        this.copyToClipboard(url)
      }
    },

    copyToClipboard(text) {
      if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
          ElMessage.success('链接已复制到剪贴板')
        }).catch(() => {
          ElMessage.error('复制失败，请手动复制链接')
        })
      } else {
        // 降级处理
        const textArea = document.createElement('textarea')
        textArea.value = text
        document.body.appendChild(textArea)
        textArea.select()
        try {
          document.execCommand('copy')
          ElMessage.success('链接已复制到剪贴板')
        } catch (err) {
          ElMessage.error('复制失败，请手动复制链接')
        }
        document.body.removeChild(textArea)
      }
    },

    formatDate(date) {
      if (!date) return ''
      const d = new Date(date)
      return d.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  },
  
  computed: {
    articleId() {
      return this.$route.params.id
    },
    
    canEdit() {
      const authStore = useAuthStore()
      // console.log(authStore.user && this.article && this.article.author &&
      //        (authStore.user.id === this.article.author?.id || authStore.user.is_admin))
      return authStore.fetchCurrentUser.user && this.article && this.article.author &&
             (authStore.user.id === this.article.author?.id || authStore.user.is_admin)
    },
    
    renderedContent() {
      if (!this.article?.content) return ''
      
      // 简单的内容渲染（实际项目中建议使用专业的markdown解析器）
      return this.article.content
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1" class="content-image">')
        .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
    }
  },
  
  async created() {
    await this.loadArticle()
  },
  

}
</script>

<style scoped>
.article-detail {
  max-width: 900px;
  margin: 0 auto;
}

.loading-container,
.error-container {
  padding: 40px 20px;
}

.article-container {
  background: linear-gradient(145deg, #4a5568 0%, #2d3748 100%);
  border-radius: 16px;
  padding: 40px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    0 4px 16px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  position: relative;
}

.article-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(145deg, rgba(152, 251, 152, 0.02), rgba(176, 224, 230, 0.02));
  border-radius: 16px;
  pointer-events: none;
}

.article-header {
  margin-bottom: 40px;
}

.breadcrumb {
  margin-bottom: 20px;
}

.breadcrumb :deep(.el-breadcrumb__item) {
  color: rgba(255, 255, 255, 0.7);
}

.breadcrumb :deep(.el-breadcrumb__item:last-child) {
  color: #98FB98;
}

.breadcrumb :deep(.el-breadcrumb__inner) {
  color: inherit;
}

.breadcrumb :deep(.el-breadcrumb__inner:hover) {
  color: #B0E0E6;
}

.article-title {
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 24px 0;
  line-height: 1.4;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.meta-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-avatar {
  background: #87CEEB;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.author-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.author-name {
  font-weight: 600;
  color: #ffffff;
}

.publish-info {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.separator {
  margin: 0 8px;
}

.article-actions {
  display: flex;
  gap: 8px;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.category-tag {
  background: rgba(152, 251, 152, 0.15);
  border: 1px solid rgba(152, 251, 152, 0.3);
  color: #98FB98;
  backdrop-filter: blur(5px);
}

.tag-item {
  background: rgba(176, 224, 230, 0.15);
  color: #B0E0E6;
  border: 1px solid rgba(176, 224, 230, 0.3);
  backdrop-filter: blur(5px);
}

.article-summary {
  background: linear-gradient(145deg, rgba(152, 251, 152, 0.1), rgba(176, 224, 230, 0.1));
  border-left: 4px solid #98FB98;
  padding: 20px;
  margin-bottom: 30px;
  font-size: 16px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.9);
  border-radius: 0 8px 8px 0;
  backdrop-filter: blur(10px);
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.article-content {
  font-size: 16px;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 40px;
}


.article-content :deep(img.content-image) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 16px 0;
  display: block;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.article-content :deep(code) {
  background: rgba(0, 0, 0, 0.3);
  color: #98FB98;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  border: 1px solid rgba(152, 251, 152, 0.3);
}

.article-content :deep(a) {
  color: #B0E0E6;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-bottom-color 0.2s;
}

.article-content :deep(a:hover) {
  border-bottom-color: #B0E0E6;
  color: #98FB98;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.7);
}

.article-stats {
  display: flex;
  gap: 24px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
}

.stat-item .el-icon {
  color: #98FB98;
}

@media (max-width: 768px) {
  .article-container {
    margin: 12px;
    padding: 24px;
    border-radius: 8px;
  }
  
  .article-title {
    font-size: 24px;
  }
  
  .article-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .article-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .article-stats {
    flex-direction: column;
    gap: 8px;
  }
}
</style>