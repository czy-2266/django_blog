<template>
  <div class="register-container">
    <el-card class="register-card" shadow="always">
      <template #header>
        <div class="card-header">
          <h2><el-icon><UserFilled /></el-icon> 用户注册</h2>
        </div>
      </template>
      
      <el-form
        ref="registerForm"
        :model="form"
        :rules="rules"
        label-width="80px"
        @submit.prevent="handleRegister"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名(3-50个字符)"
            :prefix-icon="User"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="form.email"
            placeholder="请输入邮箱地址(可选)"
            :prefix-icon="Message"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码(6-100个字符)"
            :prefix-icon="Lock"
            show-password
            clearable
          />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            :prefix-icon="Lock"
            show-password
            clearable
            @keyup.enter="handleRegister"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            :loading="authStore.isLoading"
            @click="handleRegister"
            style="width: 100%"
          >
            <el-icon v-if="!authStore.isLoading"><UserFilled /></el-icon>
            {{ authStore.isLoading ? '注册中...' : '注册' }}
          </el-button>
        </el-form-item>
        
        <el-form-item>
          <div class="register-footer">
            <span>已有账号？</span>
            <router-link to="/login" class="login-link">
              立即登录
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
import {Lock, User, UserFilled} from '@element-plus/icons-vue'

export default {
  name: 'UserRegister',
  components: {
    UserFilled
  },
  setup() {
    const authStore = useAuthStore()
    return { authStore,
            User,
            Lock
    }
  },
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 50, message: '用户名长度3-50个字符', trigger: 'blur' }
        ],
        email: [
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 100, message: '密码长度6-100个字符', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请再次输入密码', trigger: 'blur' },
          { validator: this.validateConfirmPassword, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    validateConfirmPassword(rule, value, callback) {
      if (value !== this.form.password) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    },
    async handleRegister() {
      try {
        const valid = await this.$refs.registerForm.validate()
        if (!valid) return
        
        const userData = {
          username: this.form.username,
          password: this.form.password
        }
        
        if (this.form.email) {
          userData.email = this.form.email
        }
        
        const result = await this.authStore.register(userData)
        
        if (result.success) {
          ElMessage.success('注册成功！请登录')
          await this.$router.push('/login')
        } else {
          console.log(result.error || '注册失败')
          ElMessage.error(result.error || '注册失败')
        }
      } catch (error) {
        console.error('注册错误:', error)
        ElMessage.error('注册过程中出现错误')
      }
    }
  }
}
</script>