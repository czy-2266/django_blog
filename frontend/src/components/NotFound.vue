<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <div class="error-code">404</div>
      <div class="error-message">
        <h2>页面未找到</h2>
        <p>抱歉，您访问的页面不存在或已被移动。</p>
      </div>
      <div class="action-buttons">
        <el-button type="primary" @click="goHome">
          <el-icon><House /></el-icon>
          返回首页
        </el-button>
        <el-button @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回上页
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { House, ArrowLeft } from '@element-plus/icons-vue'

export default {
  name: 'NotFound',
  components: {
    House,
    ArrowLeft
  },
  methods: {
    goHome() {
      this.$router.push('/home')
    },
    goBack() {
      this.$router.go(-1)
    }
  }
}
</script>

<style scoped>
.not-found-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.not-found-content {
  text-align: center;
  padding: 2rem;
}

.error-code {
  font-size: 8rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.error-message h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: white;
}

.error-message p {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.action-buttons .el-button {
  padding: 12px 24px;
  font-size: 1rem;
}
</style>