<template>
  <div class="theme-demo">
    <div class="demo-container">
      <h1 class="demo-title">
        <el-icon><Star /></el-icon>
        Ice BLOG 浅天蓝色主题预览
      </h1>
      
      <!-- 颜色面板 -->
      <el-card class="color-panel" shadow="hover">
        <template #header>
          <h3>主题色彩</h3>
        </template>
        <div class="color-grid">
          <div class="color-item">
            <div class="color-box primary"></div>
            <span>主色调 (#B0E0E6)</span>
          </div>
          <div class="color-item">
            <div class="color-box primary-light"></div>
            <span>浅主色 (#E0F6FF)</span>
          </div>
          <div class="color-item">
            <div class="color-box primary-dark"></div>
            <span>深主色 (#87CEEB)</span>
          </div>
          <div class="color-item">
            <div class="color-box accent"></div>
            <span>强调色 (#90CDF4)</span>
          </div>
        </div>
      </el-card>

      <!-- 组件预览 -->
      <el-card class="component-demo" shadow="hover">
        <template #header>
          <h3>组件预览</h3>
        </template>
        
        <!-- 按钮组 -->
        <div class="demo-section">
          <h4>按钮组件</h4>
          <div class="button-group">
            <el-button type="primary">主要按钮</el-button>
            <el-button type="success">成功按钮</el-button>
            <el-button type="info">信息按钮</el-button>
            <el-button type="warning">警告按钮</el-button>
            <el-button type="danger">危险按钮</el-button>
          </div>
        </div>

        <!-- 表单组件 -->
        <div class="demo-section">
          <h4>表单组件</h4>
          <el-form :model="demoForm" label-width="80px">
            <el-form-item label="用户名">
              <el-input v-model="demoForm.username" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="demoForm.email" placeholder="请输入邮箱"></el-input>
            </el-form-item>
            <el-form-item label="分类">
              <el-select v-model="demoForm.category" placeholder="请选择分类">
                <el-option label="技术分享" value="tech"></el-option>
                <el-option label="生活随笔" value="life"></el-option>
                <el-option label="项目展示" value="project"></el-option>
              </el-select>
            </el-form-item>
          </el-form>
        </div>

        <!-- 标签组 -->
        <div class="demo-section">
          <h4>标签组件</h4>
          <div class="tag-group">
            <el-tag>默认标签</el-tag>
            <el-tag type="primary">主要标签</el-tag>
            <el-tag type="success">成功标签</el-tag>
            <el-tag type="info">信息标签</el-tag>
            <el-tag type="warning">警告标签</el-tag>
            <el-tag type="danger">危险标签</el-tag>
          </div>
        </div>

        <!-- 提示消息 -->
        <div class="demo-section">
          <h4>消息提示</h4>
          <div class="button-group">
            <el-button @click="showMessage('success')">成功消息</el-button>
            <el-button @click="showMessage('info')">信息消息</el-button>
            <el-button @click="showMessage('warning')">警告消息</el-button>
            <el-button @click="showMessage('error')">错误消息</el-button>
          </div>
        </div>

        <!-- 进度条 -->
        <div class="demo-section">
          <h4>进度条</h4>
          <el-progress :percentage="70" status="success"></el-progress>
          <el-progress :percentage="50" color="#B0E0E6"></el-progress>
          <el-progress :percentage="80" color="#90CDF4"></el-progress>
        </div>

      </el-card>

      <!-- 卡片预览 -->
      <div class="card-demo-grid">
        <el-card class="demo-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>文章卡片示例</span>
              <el-tag type="primary">技术</el-tag>
            </div>
          </template>
          <h4>浅天蓝色主题设计指南</h4>
          <p>Ice BLOG采用了温和的浅天蓝色作为主色调，营造出清新、舒适的视觉体验。这种配色方案既保持了专业性，又带有一种轻松愉悦的氛围。</p>
          <div class="card-footer">
            <span class="author">设计师</span>
            <span class="date">2025-08-29</span>
          </div>
        </el-card>

        <el-card class="demo-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>用户体验</span>
              <el-tag type="success">推荐</el-tag>
            </div>
          </template>
          <h4>主题色彩心理学</h4>
          <p>浅天蓝色能够带来宁静、信任和专业的感觉。它不像深色那样严肃，也不像亮色那样刺眼，是一种非常平衡的选择。</p>
          <div class="card-footer">
            <span class="author">用户体验师</span>
            <span class="date">2025-08-29</span>
          </div>
        </el-card>
      </div>

    </div>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import { Star } from '@element-plus/icons-vue'

export default {
  name: 'ThemeDemo',
  components: {
    Star
  },
  data() {
    return {
      demoForm: {
        username: '',
        email: '',
        category: ''
      }
    }
  },
  methods: {
    showMessage(type) {
      const messages = {
        success: '操作成功！浅天蓝色主题很棒吧？',
        info: '这是一条信息提示，展示浅天蓝色主题效果',
        warning: '这是一条警告信息，注意查看颜色效果',
        error: '这是一条错误信息，即使是错误也很温和'
      }
      
      ElMessage({
        message: messages[type],
        type: type,
        duration: 3000
      })
    }
  }
}
</script>

<style scoped>
.theme-demo {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.demo-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.demo-title {
  text-align: center;
  font-size: 32px;
  color: #2D3748;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.demo-title .el-icon {
  font-size: 36px;
  color: #B0E0E6;
}

.color-panel {
  border-radius: 12px;
}

.color-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.color-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.color-box {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.color-box.primary {
  background-color: #B0E0E6;
}

.color-box.primary-light {
  background-color: #E0F6FF;
}

.color-box.primary-dark {
  background-color: #87CEEB;
}

.color-box.accent {
  background-color: #90CDF4;
}

.component-demo {
  border-radius: 12px;
}

.demo-section {
  margin-bottom: 30px;
}

.demo-section h4 {
  margin-bottom: 16px;
  color: #2D3748;
  font-size: 18px;
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.tag-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.card-demo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
}

.demo-card {
  border-radius: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.demo-card h4 {
  color: #2D3748;
  margin-bottom: 12px;
  font-size: 16px;
}

.demo-card p {
  color: #4A5568;
  line-height: 1.6;
  margin-bottom: 16px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #718096;
}

@media (max-width: 768px) {
  .theme-demo {
    padding: 15px;
  }
  
  .demo-title {
    font-size: 24px;
  }
  
  .color-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .card-demo-grid {
    grid-template-columns: 1fr;
  }
  
  .button-group {
    flex-direction: column;
    align-items: stretch;
  }
  
  .button-group .el-button {
    margin: 0;
  }
}
</style>