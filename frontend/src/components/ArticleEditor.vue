<template>
  <div class="article-editor">
    <div class="editor-header">
      <h1 v-if="isEdit">
        <el-icon><Edit /></el-icon>
        编辑文章
      </h1>
      <h1 v-else>
        <el-icon><EditPen /></el-icon>
        发布文章
      </h1>
      
      <div class="header-actions">
        <el-button @click="saveDraft" :loading="saving">
          <el-icon><Collection /></el-icon>
          保存草稿
        </el-button>
        <el-button type="primary" @click="publishArticle" :loading="publishing">
          <el-icon><Promotion /></el-icon>
          {{ isEdit ? '更新文章' : '发布文章' }}
        </el-button>
      </div>
    </div>

    <div class="editor-container">
      <el-form
        ref="articleForm"
        :model="form"
        :rules="rules"
        label-width="80px"
        class="article-form"
      >
        <!-- 文章标题 -->
        <el-form-item label="文章标题" prop="title" class="title-item">
          <el-input
            v-model="form.title"
            placeholder="请输入文章标题（建议50字以内）"
            maxlength="100"
            show-word-limit
            size="large"
            clearable
          />
        </el-form-item>

        <!-- 文章摘要 -->
        <el-form-item label="文章摘要" prop="summary">
          <el-input
            v-model="form.summary"
            type="textarea"
            :rows="3"
            placeholder="请输入文章摘要（可选，建议200字以内）"
            maxlength="300"
            show-word-limit
          />
        </el-form-item>

        <!-- 分类选择 -->
        <el-form-item label="文章分类" prop="category_id">
          <div class="category-selector">
            <el-select
              v-model="form.category_id"
              placeholder="选择文章分类"
              filterable
              style="width: 200px"
            >
              <el-option
                v-for="category in categories"
                :key="category?.id"
                :label="category?.name"
                :value="category?.id"
              />
            </el-select>
            <el-button @click="showCategoryDialog = true" text type="primary">
              <el-icon><Plus /></el-icon>
              新建分类
            </el-button>
          </div>
        </el-form-item>

        <!-- 文章内容 -->
        <el-form-item label="文章内容" prop="content" class="content-item">
          <div class="editor-toolbar">
            <el-button-group>
              <el-button @click="insertImage" size="small">
                <el-icon><Picture /></el-icon>
                插入图片
              </el-button>
              <el-button @click="insertFile" size="small">
                <el-icon><Document /></el-icon>
                插入文件
              </el-button>
              <el-button @click="togglePreview" size="small" :type="previewMode ? 'primary' : ''">
                <el-icon><View /></el-icon>
                {{ previewMode ? '编辑模式' : '预览模式' }}
              </el-button>
            </el-button-group>
          </div>

          <!-- 文本编辑器 -->
          <div class="content-editor">
            <el-input
              v-show="!previewMode"
              v-model="form.content"
              type="textarea"
              :rows="20"
              placeholder="开始写作你的文章内容..."
              class="content-textarea"
            />
            
            <!-- Markdown预览 -->
            <div v-show="previewMode" class="content-preview" v-html="renderedContent"></div>
          </div>
        </el-form-item>

        <!-- 文章标签 -->
        <el-form-item label="文章标签">
          <el-tag
            v-for="tag in form.tags"
            :key="tag"
            closable
            @close="removeTag(tag)"
            class="tag-item"
          >
            {{ tag }}
          </el-tag>
          <el-input
            v-if="inputVisible"
            ref="tagInput"
            v-model="inputValue"
            size="small"
            style="width: 100px"
            @keyup.enter="handleInputConfirm"
            @blur="handleInputConfirm"
          />
          <el-button v-else @click="showInput" size="small" text>
            <el-icon><Plus /></el-icon>
            添加标签
          </el-button>
        </el-form-item>

        <!-- 发布状态 -->
        <el-form-item label="发布状态" v-if="!isEdit">
          <el-radio-group v-model="form.is_published">
            <el-radio :label="true">立即发布</el-radio>
            <el-radio :label="false">保存为草稿</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
    </div>

    <!-- 新建分类对话框 -->
    <el-dialog
      v-model="showCategoryDialog"
      title="新建分类"
      width="400px"
      :close-on-click-modal="false"
    >
      <el-form :model="categoryForm" :rules="categoryRules" ref="categoryFormRef">
        <el-form-item label="分类名称" prop="name">
          <el-input
            v-model="categoryForm.name"
            placeholder="请输入分类名称"
            maxlength="50"
          />
        </el-form-item>
        <el-form-item label="分类描述" prop="description">
          <el-input
            v-model="categoryForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入分类描述（可选）"
            maxlength="200"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showCategoryDialog = false">取消</el-button>
          <el-button type="primary" @click="createCategory" :loading="creatingCategory">
            创建
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 文件上传组件（隐藏） -->
    <input
      ref="imageInput"
      type="file"
      accept="image/*"
      multiple
      style="display: none"
      @change="handleImageUpload"
    />
    <input
      ref="fileInput"
      type="file"
      multiple
      style="display: none"
      @change="handleFileUpload"
    />
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import {
  Edit,
  EditPen,
  Collection,
  Promotion,
  Plus,
  Picture,
  Document,
  View
} from '@element-plus/icons-vue'
import { articleAPI, categoryAPI, uploadAPI } from '@/api/blog'

export default {
  name: 'ArticleEditor',
  components: {
    Edit,
    EditPen,
    Collection,
    Promotion,
    Plus,
    Picture,
    Document,
    View
  },
  
  data() {
    return {
      form: {
        title: '',
        summary: '',
        content: '',
        category_id: null,
        is_published: true,
        tags: []
      },
      
      categories: [],
      previewMode: false,
      saving: false,
      publishing: false,
      
      // 标签输入
      inputVisible: false,
      inputValue: '',
      
      // 新建分类
      showCategoryDialog: false,
      creatingCategory: false,
      categoryForm: {
        name: '',
        description: ''
      },
      
      rules: {
        title: [
          { required: true, message: '请输入文章标题', trigger: 'blur' },
          { min: 1, max: 100, message: '标题长度在1到100个字符', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入文章内容', trigger: 'blur' }
        ],
        category_id: [
          { required: true, message: '请选择文章分类', trigger: 'change' }
        ]
      },
      
      categoryRules: {
        name: [
          { required: true, message: '请输入分类名称', trigger: 'blur' },
          { min: 1, max: 50, message: '分类名称长度在1到50个字符', trigger: 'blur' }
        ]
      }
    }
  },
  
  computed: {
    isEdit() {
      return this.$route.name === 'ArticleEdit'
    },
    
    articleId() {
      return this.$route.params.id
    },
    
    renderedContent() {
      // 简单的Markdown渲染（实际项目中建议使用专业的markdown解析器）
      if (!this.form.content) return ''
      
      return this.form.content
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1" class="content-image">')
        .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
    }
  },
  
  async created() {
    await this.loadCategories()
    
    if (this.isEdit && this.articleId) {
      await this.loadArticle()
    }
  },
  
  methods: {
    // 加载分类列表
    async loadCategories() {
      try {
        const response = await categoryAPI.getCategories()
        // 处理Django REST Framework的分页响应格式
        this.categories = Array.isArray(response) ? response : (response.results || [])
        // 过滤掉 null 或 undefined 的分类
        this.categories = this.categories.filter(category => category != null)
      } catch (error) {
        console.error('加载分类失败:', error)
        ElMessage.error('加载分类列表失败')
        // 确保 categories 是一个空数组而不是 null
        this.categories = []
      }
    },
    
    // 加载文章详情（编辑模式）
    async loadArticle() {
      try {
        const article = await articleAPI.getArticle(this.articleId)
        this.form = {
          title: article.title || '',
          summary: article.summary || '',
          content: article.content || '',
          category_id: article.category_id || null,
          is_published: article.is_published || false,
          tags: article.tags || []
        }
      } catch (error) {
        console.error('加载文章失败:', error)
        ElMessage.error('加载文章失败')
        this.$router.push('/articles')
      }
    },
    
    // 保存草稿
    async saveDraft() {
      const isValid = await this.$refs.articleForm.validate().catch(() => false)
      if (!isValid) return
      
      try {
        this.saving = true
        const data = { ...this.form, is_published: false }
        
        if (this.isEdit) {
          await articleAPI.updateArticle(this.articleId, data)
          ElMessage.success('草稿保存成功')
        } else {
          await articleAPI.createArticle(data)
          ElMessage.success('草稿保存成功')
          // this.$router.replace(`/articles/edit/${article.id || article.data.id}`)
        }
      } catch (error) {
        console.error('保存草稿失败:', error)
        ElMessage.error('保存草稿失败，请重试')
      } finally {
        this.saving = false
      }
    },
    
    // 发布文章
    async publishArticle() {
      const isValid = await this.$refs.articleForm.validate().catch(() => false)
      if (!isValid) return
      
      try {
        this.publishing = true
        const data = { ...this.form, is_published: true }
        
        if (this.isEdit) {
          await articleAPI.updateArticle(this.articleId, data)
          ElMessage.success('文章更新成功')
        } else {
          await articleAPI.createArticle(data)
          ElMessage.success('文章发布成功')
          // this.$router.push(`/articles/${article.id || article.data.id}`)
          return
        }
        
        this.$router.push(`/articles/${this.articleId}`)
      } catch (error) {
        console.error('发布文章失败:', error)
        ElMessage.error('发布文章失败，请重试')
      } finally {
        this.publishing = false
      }
    },
    
    // 创建新分类
    async createCategory() {
      const isValid = await this.$refs.categoryFormRef.validate().catch(() => false)
      if (!isValid) return
      
      try {
        this.creatingCategory = true
        const category = await categoryAPI.createCategory(this.categoryForm)
        // 确保 category 不是 null
        if (category) {
          this.categories.push(category)
          this.form.category_id = category.id
        }
        this.showCategoryDialog = false
        this.categoryForm = { name: '', description: '' }
        ElMessage.success('分类创建成功')
      } catch (error) {
        console.error('创建分类失败:', error)
        ElMessage.error('创建分类失败，请重试')
      } finally {
        this.creatingCategory = false
      }
    },
    
    // 切换预览模式
    togglePreview() {
      this.previewMode = !this.previewMode
    },
    
    // 插入图片
    insertImage() {
      this.$refs.imageInput.click()
    },
    
    // 插入文件
    insertFile() {
      this.$refs.fileInput.click()
    },
    
    // 处理图片上传
    async handleImageUpload(event) {
      const files = Array.from(event.target.files)
      if (files.length === 0) return
      
      try {
        for (const file of files) {
          await uploadAPI.uploadFile(file)
          // const imageUrl = response.url
          // const imageMarkdown = `![${file.name}](${imageUrl})\n`
          // this.insertTextAtCursor(imageMarkdown)
        }
        ElMessage.success(`成功上传 ${files.length} 张图片`)
      } catch (error) {
        console.error('图片上传失败:', error)
        ElMessage.error('图片上传失败，请重试')
      } finally {
        event.target.value = '' // 清空input
      }
    },
    
    // 处理文件上传
    async handleFileUpload(event) {
      const files = Array.from(event.target.files)
      if (files.length === 0) return
      
      try {
        for (const file of files) {
          await uploadAPI.uploadFile(file)
          // const fileUrl = response.url
          // const fileMarkdown = `[${file.name}](${fileUrl})\n`
          // this.insertTextAtCursor(fileMarkdown)
        }
        ElMessage.success(`成功上传 ${files.length} 个文件`)
      } catch (error) {
        console.error('文件上传失败:', error)
        ElMessage.error('文件上传失败，请重试')
      } finally {
        event.target.value = '' // 清空input
      }
    },
    
    // 在光标位置插入文本
    insertTextAtCursor(text) {
      const textarea = this.$el.querySelector('.content-textarea textarea')
      if (textarea) {
        const start = textarea.selectionStart
        const end = textarea.selectionEnd
        const content = this.form.content
        this.form.content = content.substring(0, start) + text + content.substring(end)
        
        // 设置光标位置
        this.$nextTick(() => {
          textarea.focus()
          textarea.setSelectionRange(start + text.length, start + text.length)
        })
      } else {
        this.form.content += text
      }
    },
    
    // 标签管理
    removeTag(tag) {
      this.form.tags = this.form.tags.filter(t => t !== tag)
    },
    
    showInput() {
      this.inputVisible = true
      this.$nextTick(() => {
        this.$refs.tagInput.focus()
      })
    },
    
    handleInputConfirm() {
      const value = this.inputValue.trim()
      if (value && !this.form.tags.includes(value)) {
        this.form.tags.push(value)
      }
      this.inputVisible = false
      this.inputValue = ''
    }
  },
  

}
</script>

<style scoped>
.article-editor {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.editor-header h1 {
  margin: 0;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.article-form {
  max-width: 100%;
}

.title-item :deep(.el-form-item__content) {
  width: 100%;
}

.content-item :deep(.el-form-item__content) {
  width: 100%;
}

.category-selector {
  display: flex;
  align-items: center;
  gap: 12px;
}

.editor-toolbar {
  margin-bottom: 12px;
}

.content-editor {
  position: relative;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  overflow: hidden;
}

.content-textarea :deep(textarea) {
  border: none !important;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  line-height: 1.6;
  resize: vertical;
}

.content-preview {
  padding: 12px;
  min-height: 400px;
  background: #fafafa;
  line-height: 1.8;
  font-size: 14px;
  color: #2c3e50;
}

.content-preview :deep(code) {
  background: #f1f2f3;
  padding: 2px 4px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.tag-item {
  margin-right: 8px;
  margin-bottom: 8px;
}

@media (max-width: 768px) {
  .article-editor {
    margin: 12px;
    padding: 16px;
  }
  
  .editor-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .category-selector {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>