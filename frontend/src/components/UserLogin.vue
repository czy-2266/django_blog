<template>
  <div class="login-container">
    <el-card class="login-card" shadow="always">
      <template #header>
        <div class="card-header">
          <h2><el-icon><User /></el-icon> 用户登录</h2>
        </div>
      </template>
      
      <el-form
        ref="loginForm"
        :model="form"
        :rules="rules"
        label-width="80px"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            :prefix-icon="User"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
            clearable
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            :loading="authStore.isLoading"
            @click="handleLogin"
            style="width: 100%"
          >
            <el-icon v-if="!authStore.isLoading"><Lock /></el-icon>
            {{ authStore.isLoading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
        
        <el-form-item>
          <div class="login-footer">
            <span>还没有账号？</span>
            <router-link to="/register" class="register-link">
              立即注册
            </router-link>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

export default {
  name: 'UserLogin',
  components: {
    User,
    Lock
  },
  setup() {
    const authStore = useAuthStore()
    return {
      authStore,
      User,
      Lock
    }
  },
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 50, message: '用户名长度3-50个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 100, message: '密码长度6-100个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    async handleLogin() {
      try {
        const valid = await this.$refs.loginForm.validate()
        if (!valid) return
        
        const result = await this.authStore.login(this.form)
        
        if (result.success) {
          ElMessage.success('登录成功！')
          await this.$router.push('/profile')
        } else {
          ElMessage.error(result.error || '登录失败')
        }
      } catch (error) {
        console.error('登录错误:', error)
        ElMessage.error('登录过程中出现错误')
      }
    }
  }
}
</script>