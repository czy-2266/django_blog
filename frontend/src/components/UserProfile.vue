<template>
  <div class="profile-container">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="16" :md="12" :lg="8" :xl="6">
        <el-card class="profile-card" shadow="always">
          <template #header>
            <div class="card-header">
              <h2><el-icon><Avatar /></el-icon> 个人中心</h2>
            </div>
          </template>
          
          <!-- 用户信息展示 -->
          <div v-if="!isEditing" class="user-info">
            <!-- 头像区域 -->
            <div class="avatar-section">
              <div class="avatar-container" @click="triggerAvatarUpload">
                <el-avatar 
                  :size="120" 
                  :src="authStore.user?.avatar_url" 
                  class="user-avatar"
                >
                  <span class="avatar-text">
                    {{ authStore.user?.username?.charAt(0)?.toUpperCase() }}
                  </span>
                </el-avatar>
                <div class="avatar-overlay">
                  <el-icon><Camera /></el-icon>
                  <span>修改头像</span>
                </div>
              </div>
              <input
                ref="avatarInput"
                type="file"
                accept="image/*"
                style="display: none"
                @change="handleAvatarUpload"
              />
            </div>
            
            <div class="info-item">
              <label>用户名：</label>
              <span>{{ authStore.user?.username }}</span>
            </div>
            <div class="info-item">
              <label>邮箱：</label>
              <span>{{ authStore.user?.email || '未设置' }}</span>
            </div>
            <div class="info-item">
              <label>个人简介：</label>
              <span>{{ authStore.user?.bio || '这个人很懒，什么都没有留下' }}</span>
            </div>
            <div class="info-item">
              <label>注册时间：</label>
              <span>{{ formatDate(authStore.user?.created_at) }}</span>
            </div>
            <div class="info-item">
              <label>状态：</label>
              <el-tag :type="authStore.user?.is_active ? 'success' : 'danger'">
                {{ authStore.user?.is_active ? '正常' : '禁用' }}
              </el-tag>
            </div>
            
            <div class="action-buttons">
              <el-button type="primary" @click="startEdit">
                <el-icon><Edit /></el-icon>
                编辑资料
              </el-button>
            </div>
          </div>
          
          <!-- 编辑表单 -->
          <el-form
            v-if="isEditing"
            ref="editForm"
            :model="editForm"
            :rules="rules"
            label-width="80px"
          >
            <el-form-item label="用户名" prop="username">
              <el-input
                v-model="editForm.username"
                placeholder="请输入用户名"
                clearable
              />
            </el-form-item>
            
            <el-form-item label="邮箱" prop="email">
              <el-input
                v-model="editForm.email"
                placeholder="请输入邮箱地址"
                clearable
              />
            </el-form-item>
            
            <el-form-item label="新密码" prop="password">
              <el-input
                v-model="editForm.password"
                type="password"
                placeholder="不修改请留空"
                show-password
                clearable
              />
            </el-form-item>
            
            <div class="action-buttons">
              <el-button 
                type="primary" 
                :loading="authStore.isLoading"
                @click="handleUpdate"
              >
                <el-icon v-if="!authStore.isLoading"><Check /></el-icon>
                {{ authStore.isLoading ? '更新中...' : '保存' }}
              </el-button>
              <el-button @click="cancelEdit">
                <el-icon><Close /></el-icon>
                取消
              </el-button>
            </div>
          </el-form>
        </el-card>
      </el-col>
      
      <!-- 可以在这里添加更多卡片，比如活动历史、设置等 -->
    </el-row>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { ElMessage } from 'element-plus'
import { Avatar, Edit, Check, Close, Camera } from '@element-plus/icons-vue'
import { userAPI } from '@/api/blog'

export default {
  name: 'UserProfile',
  components: {
    Avatar,
    Edit,
    Check,
    Close,
    Camera
  },
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
  data() {
    return {
      isEditing: false,
      editForm: {
        username: '',
        email: '',
        password: ''
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
          { min: 6, max: 100, message: '密码长度6-100个字符', trigger: 'blur' }
        ]
      }
    }
  },
  async created() {
    // 确保用户信息已加载
    if (!this.authStore.user) {
      await this.authStore.fetchCurrentUser()
    }
    
    // 如果仍然没有用户信息，重定向到登录页
    if (!this.authStore.user) {
      ElMessage.error('未能获取用户信息，请重新登录')
      await this.$router.push('/login')
    }
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleString('zh-CN')
    },
    
    startEdit() {
      this.isEditing = true
      this.editForm = {
        username: this.authStore.user?.username || '',
        email: this.authStore.user?.email || '',
        password: ''
      }
    },
    
    cancelEdit() {
      this.isEditing = false
      this.editForm = {
        username: '',
        email: '',
        password: ''
      }
    },
    
    // 头像上传方法
    triggerAvatarUpload() {
      this.$refs.avatarInput.click()
    },
    
    async handleAvatarUpload(event) {
      const file = event.target.files[0]
      if (!file) return
      
      if (!file.type.startsWith('image/')) {
        ElMessage.error('请选择图片文件')
        return
      }
      
      if (file.size > 10 * 1024 * 1024) {
        ElMessage.error('头像文件大小不能超过10MB')
        return
      }
      
      try {
        await userAPI.uploadAvatar(file)
        await this.authStore.fetchCurrentUser()
        ElMessage.success('头像更新成功')
      } catch (error) {
        console.error('头像上传失败:', error)
        ElMessage.error('头像上传失败，请重试')
      } finally {
        event.target.value = ''
      }
    },
    
    async handleUpdate() {
      try {
        const valid = await this.$refs.editForm.validate()
        if (!valid) return
        
        // 准备更新数据
        const updateData = {
          username: this.editForm.username,
          email: this.editForm.email || null
        }
        
        // 如果输入了新密码，则包含在更新中
        if (this.editForm.password) {
          updateData.password = this.editForm.password
        }
        
        const result = await this.authStore.updateUser(updateData)
        
        if (result.success) {
          ElMessage.success('更新资料成功！')
          this.isEditing = false
        } else {
          ElMessage.error(result.error || '更新失败')
        }
      } catch (error) {
        console.error('更新错误:', error)
        ElMessage.error('更新过程中出现错误')
      }
    }
  }
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-card {
  border-radius: 12px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-header h2 {
  margin: 0;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 8px;
}

.avatar-section {
  text-align: center;
  margin-bottom: 24px;
}

.avatar-container {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.user-avatar {
  background: linear-gradient(135deg, #87CEEB, #4682B4);
  transition: all 0.3s ease;
}

.avatar-text {
  font-size: 48px;
  font-weight: bold;
  color: white;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  color: white;
  font-size: 12px;
  gap: 4px;
}

.avatar-container:hover .avatar-overlay {
  opacity: 1;
}

.info-item {
  display: flex;
  margin-bottom: 16px;
  align-items: center;
}

.info-item label {
  font-weight: 500;
  color: #606266;
  width: 100px;
  flex-shrink: 0;
}

.action-buttons {
  margin-top: 24px;
  text-align: center;
}

.action-buttons .el-button {
  margin-right: 12px;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}
</style>