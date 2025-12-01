<template>
  <div class="effects-guide" v-if="showGuide">
    <div class="guide-overlay" @click="closeGuide"></div>
    <div class="guide-content">
      <div class="guide-header">
        <h2>
          <el-icon><MagicStick /></el-icon>
          Ice BLOG 视觉效果指南
        </h2>
        <el-button @click="closeGuide" :icon="Close" circle size="small"></el-button>
      </div>
      
      <div class="guide-body">
        <div class="feature-section">
          <h3>
            <el-icon><Star /></el-icon>
            点击星星效果
          </h3>
          <p>在页面任意位置点击鼠标，将会出现天蓝色的星星爆发效果！</p>
          <div class="demo-area" @click="demoClick">
            <span>👆 点击这里试试看！</span>
          </div>
        </div>
        
        <div class="feature-section">
          <h3>
            <el-icon><Picture /></el-icon>
            背景图片轮换
          </h3>
          <p>页面底部会自动轮换显示美丽的壁纸，营造优雅的视觉氛围。</p>
          <div class="slideshow-preview">
            <div class="preview-images">
              <div 
                v-for="(image, index) in previewImages" 
                :key="index"
                class="preview-image"
                :class="{ active: previewIndex === index }"
                :style="{ backgroundImage: `url(${image})` }"
              ></div>
            </div>
          </div>
        </div>
        
        <div class="feature-section">
          <h3>
            <el-icon><Setting /></el-icon>
            自定义控制
          </h3>
          <p>使用右侧的控制面板，您可以：</p>
          <ul class="feature-list">
            <li>🎛️ 开启/关闭各种视觉效果</li>
            <li>⏱️ 调整图片轮换速度</li>
            <li>✨ 设置特效强度级别</li>
            <li>🔄 一键重置所有设置</li>
          </ul>
        </div>
        
        <div class="tips-section">
          <h3>
            <el-icon><InfoFilled /></el-icon>
            温馨提示
          </h3>
          <div class="tips-grid">
            <div class="tip-item">
              <el-icon class="tip-icon"><Cpu /></el-icon>
              <span>视觉效果经过性能优化，不会影响浏览体验</span>
            </div>
            <div class="tip-item">
              <el-icon class="tip-icon"><Phone /></el-icon>
              <span>在移动设备上自动调整效果强度</span>
            </div>
            <div class="tip-item">
              <el-icon class="tip-icon"><Lock /></el-icon>
              <span>您的设置会自动保存到本地存储</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="guide-footer">
        <el-checkbox v-model="dontShowAgain">不再显示此指南</el-checkbox>
        <el-button type="primary" @click="closeGuide">
          开始体验
          <el-icon><Right /></el-icon>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { 
  MagicStick, Close, Star, Picture, Setting, InfoFilled, 
  Cpu, Phone, Lock, Right 
} from '@element-plus/icons-vue'

// 导入预览图片
import preview1 from '@/assets/【哲风壁纸】傍晚路灯-山脉-水面.png'
import preview2 from '@/assets/【哲风壁纸】城市-大海-天空.png'
import preview3 from '@/assets/【哲风壁纸】夜景-富士山.png'

export default {
  name: 'EffectsGuide',
  components: {
    MagicStick, Close, Star, Picture, Setting, InfoFilled,
    Cpu, Phone, Lock, Right
  },
  data() {
    return {
      showGuide: false,
      dontShowAgain: false,
      previewImages: [
        preview1,
        preview2,
        preview3
      ],
      previewIndex: 0,
      previewTimer: null
    }
  },
  mounted() {
    // 检查是否应该显示指南
    const hasSeenGuide = localStorage.getItem('iceBlogEffectsGuideShown')
    if (!hasSeenGuide) {
      setTimeout(() => {
        this.showGuide = true
        this.startPreviewSlideshow()
      }, 1000)
    }
  },
  beforeUnmount() {
    if (this.previewTimer) {
      clearInterval(this.previewTimer)
    }
  },
  methods: {
    closeGuide() {
      this.showGuide = false
      if (this.dontShowAgain) {
        localStorage.setItem('iceBlogEffectsGuideShown', 'true')
      }
      if (this.previewTimer) {
        clearInterval(this.previewTimer)
      }
    },
    
    demoClick(event) {
      // 触发演示点击效果
      this.$emit('demo-click', {
        clientX: event.clientX,
        clientY: event.clientY
      })
    },
    
    startPreviewSlideshow() {
      this.previewTimer = setInterval(() => {
        this.previewIndex = (this.previewIndex + 1) % this.previewImages.length
      }, 2000)
    }
  }
}
</script>

<style scoped>
.effects-guide {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.guide-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
}

.guide-content {
  position: relative;
  background: white;
  border-radius: 20px;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(176, 224, 230, 0.4);
  border: 2px solid rgba(176, 224, 230, 0.3);
}

.guide-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 30px;
  background: linear-gradient(135deg, #B0E0E6 0%, #87CEEB 100%);
  border-radius: 18px 18px 0 0;
}

.guide-header h2 {
  margin: 0;
  color: #2D3748;
  font-size: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.guide-body {
  padding: 30px;
}

.feature-section {
  margin-bottom: 30px;
}

.feature-section h3 {
  color: #2D3748;
  font-size: 18px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.feature-section h3 .el-icon {
  color: #B0E0E6;
}

.feature-section p {
  color: #4A5568;
  line-height: 1.6;
  margin-bottom: 16px;
}

.demo-area {
  background: linear-gradient(135deg, #F0F9FF 0%, #E0F6FF 100%);
  border: 2px dashed #B0E0E6;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 16px;
  color: #2D3748;
}

.demo-area:hover {
  background: linear-gradient(135deg, #E0F6FF 0%, #B0E0E6 100%);
  transform: translateY(-2px);
}

.slideshow-preview {
  border-radius: 12px;
  overflow: hidden;
  height: 120px;
  position: relative;
}

.preview-images {
  position: relative;
  width: 100%;
  height: 100%;
}

.preview-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  opacity: 0;
  transition: opacity 1s ease-in-out;
}

.preview-image.active {
  opacity: 1;
}

.feature-list {
  list-style: none;
  padding: 0;
}

.feature-list li {
  padding: 8px 0;
  color: #4A5568;
  font-size: 15px;
}

.tips-section {
  background: #F7FAFC;
  border-radius: 12px;
  padding: 20px;
  margin-top: 20px;
}

.tips-section h3 {
  color: #2D3748;
  font-size: 16px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tips-grid {
  display: grid;
  gap: 12px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #4A5568;
  font-size: 14px;
}

.tip-icon {
  color: #B0E0E6;
  font-size: 16px;
}

.guide-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 30px;
  border-top: 1px solid #E2E8F0;
  background: #F7FAFC;
  border-radius: 0 0 18px 18px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .guide-content {
    margin: 20px;
    max-width: none;
    max-height: 90vh;
  }
  
  .guide-header {
    padding: 20px;
  }
  
  .guide-header h2 {
    font-size: 20px;
  }
  
  .guide-body {
    padding: 20px;
  }
  
  .guide-footer {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
}
</style>