<template>
  <div class="about-page">
    <div class="hero-section">
      <div class="hero-content">
        <h1>
          <el-icon><Star /></el-icon>
          关于 Ice BLOG
        </h1>
        <p class="hero-subtitle">一个优雅的个人博客系统</p>
      </div>
    </div>

    <div class="content-sections">
      <!-- 项目介绍 -->
      <section class="intro-section">
        <h2>
          <el-icon><InfoFilled /></el-icon>
          项目介绍
        </h2>
        <div class="intro-content">
          <p>
            Ice BLOG 是一个基于现代Web技术栈构建的个人博客系统，致力于提供简洁、优雅、高效的写作和阅读体验。
          </p>
          <p>
            系统采用前后端分离的架构设计，前端使用 Vue 3 + Element Plus，后端采用 FastAPI + SQLAlchemy，
            支持文章发布、分类管理、全文搜索、用户认证等核心功能。
          </p>
        </div>
      </section>

      <!-- 技术栈 -->
      <section class="tech-section">
        <h2>
          <el-icon><Tools /></el-icon>
          技术栈
        </h2>
        <div class="tech-stacks">
          <div class="tech-category">
            <h3>前端技术</h3>
            <div class="tech-items">
              <div class="tech-item">
                <el-icon><DataBoard /></el-icon>
                <div>
                  <h4>Vue 3</h4>
                  <p>渐进式JavaScript框架</p>
                </div>
              </div>
              <div class="tech-item">
                <el-icon><Grid /></el-icon>
                <div>
                  <h4>Element Plus</h4>
                  <p>Vue 3 组件库</p>
                </div>
              </div>
              <div class="tech-item">
                <el-icon><Switch /></el-icon>
                <div>
                  <h4>Pinia</h4>
                  <p>Vue 状态管理</p>
                </div>
              </div>
              <div class="tech-item">
                <el-icon><Connection /></el-icon>
                <div>
                  <h4>Vue Router</h4>
                  <p>前端路由管理</p>
                </div>
              </div>
            </div>
          </div>

          <div class="tech-category">
            <h3>后端技术</h3>
            <div class="tech-items">
              <div class="tech-item">
                <el-icon><Service /></el-icon>
                <div>
                  <h4>Django</h4>
                  <p>现代化Python Web框架</p>
                </div>
              </div>
              <div class="tech-item">
                <el-icon><Coin /></el-icon>
                <div>
                  <h4>SQLAlchemy</h4>
                  <p>Python SQL工具包和ORM</p>
                </div>
              </div>
              <div class="tech-item">
                <el-icon><Lock /></el-icon>
                <div>
                  <h4>JWT</h4>
                  <p>JSON Web Token认证</p>
                </div>
              </div>
              <div class="tech-item">
                <el-icon><Files /></el-icon>
                <div>
                  <h4>MySQL</h4>
                  <p>关系型数据库</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 功能特性 -->
      <section class="features-section">
        <h2>
          <el-icon><Star /></el-icon>
          功能特性
        </h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><Edit /></el-icon>
            </div>
            <h3>文章管理</h3>
            <p>支持Markdown语法，富文本编辑，草稿保存，定时发布</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><FolderOpened /></el-icon>
            </div>
            <h3>分类管理</h3>
            <p>灵活的分类体系，支持多级分类，便于内容组织</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><Search /></el-icon>
            </div>
            <h3>全文搜索</h3>
            <p>强大的搜索功能，支持标题、内容、标签全文检索</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><Picture /></el-icon>
            </div>
            <h3>文件上传</h3>
            <p>支持图片、文档等多种文件格式上传和管理</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><User /></el-icon>
            </div>
            <h3>用户系统</h3>
            <p>完整的用户认证体系，支持注册、登录、权限管理</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><Monitor /></el-icon>
            </div>
            <h3>响应式设计</h3>
            <p>完美适配桌面端和移动端，提供一致的用户体验</p>
          </div>
        </div>
      </section>

      <!-- 开源信息 -->
      <section class="opensource-section">
        <h2>
          <el-icon><Share /></el-icon>
          开源协议
        </h2>
        <div class="opensource-content">
          <p>
            Ice BLOG 遵循 MIT 开源协议，欢迎大家使用、修改和分发。
          </p>
          <div class="github-info">
            <el-card class="github-card">
              <div class="repo-info">
                <h3>GitHub 仓库</h3>
                <p>欢迎 Star、Fork 和贡献代码</p>
                <el-button type="primary" @click="openGithub">
                  <el-icon><Link /></el-icon>
                  访问 GitHub
                </el-button>
              </div>
            </el-card>
          </div>
        </div>
      </section>

      <!-- 联系方式 -->
      <section class="contact-section">
        <h2>
          <el-icon><ChatDotRound /></el-icon>
          联系方式
        </h2>
        <div class="contact-content">
          <p>如果您有任何问题、建议或合作意向，欢迎通过以下方式联系我们：</p>
          <div class="contact-items">
            <div class="contact-item">
              <el-icon><Message /></el-icon>
              <span>邮箱：contact@iceblog.dev</span>
            </div>
            <div class="contact-item">
              <el-icon><ChatDotRound /></el-icon>
              <span>QQ群：123456789</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import {
  Star,
  InfoFilled,
  Tools,
  DataBoard,
  Grid,
  Switch,
  Connection,
  Service,
  Coin,
  Lock,
  Files,
  Edit,
  FolderOpened,
  Search,
  Picture,
  User,
  Monitor,
  Share,
  Link,
  ChatDotRound,
  Message
} from '@element-plus/icons-vue'

export default {
  name: 'AboutPage',
  components: {
    Star,
    InfoFilled,
    Tools,
    DataBoard,
    Grid,
    Switch,
    Connection,
    Service,
    Coin,
    Lock,
    Files,
    Edit,
    FolderOpened,
    Search,
    Picture,
    User,
    Monitor,
    Share,
    Link,
    ChatDotRound,
    Message
  },
  
  methods: {
    openGithub() {
      window.open('https://github.com/ice-blog/ice-blog', '_blank')
    }
  }
}
</script>

<style scoped>
.about-page {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  background: linear-gradient(135deg, #87CEEB 0%, #4682B4 100%);
  border-radius: 16px;
  padding: 80px 40px;
  text-align: center;
  margin-bottom: 40px;
  color: white;
}

.hero-content h1 {
  font-size: 48px;
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.hero-subtitle {
  font-size: 18px;
  margin: 0;
  opacity: 0.9;
}

.content-sections {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

section {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

section h2 {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #2c3e50;
  margin: 0 0 24px 0;
  font-size: 24px;
}

.intro-content p {
  line-height: 1.8;
  color: #555;
  margin-bottom: 16px;
}

.tech-stacks {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
}

.tech-category h3 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 18px;
}

.tech-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tech-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.tech-item:hover {
  border-color: #87CEEB;
  background: #f8fcff;
}

.tech-item .el-icon {
  font-size: 24px;
  color: #87CEEB;
}

.tech-item h4 {
  margin: 0 0 4px 0;
  color: #2c3e50;
}

.tech-item p {
  margin: 0;
  color: #718096;
  font-size: 14px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.feature-card {
  text-align: center;
  padding: 24px;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.feature-card:hover {
  border-color: #87CEEB;
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(135, 206, 235, 0.2);
}

.feature-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #87CEEB, #4682B4);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.feature-icon .el-icon {
  font-size: 28px;
  color: white;
}

.feature-card h3 {
  color: #2c3e50;
  margin: 0 0 12px 0;
}

.feature-card p {
  color: #718096;
  line-height: 1.6;
  margin: 0;
}

.opensource-content p {
  line-height: 1.8;
  color: #555;
  margin-bottom: 24px;
}

.github-info {
  display: flex;
  justify-content: center;
}

.github-card {
  max-width: 400px;
  text-align: center;
}

.repo-info h3 {
  margin: 0 0 12px 0;
  color: #2c3e50;
}

.repo-info p {
  color: #718096;
  margin: 0 0 20px 0;
}

.contact-content p {
  line-height: 1.8;
  color: #555;
  margin-bottom: 24px;
}

.contact-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.contact-item .el-icon {
  color: #87CEEB;
  font-size: 18px;
}

@media (max-width: 768px) {
  .about-page {
    margin: 12px;
  }
  
  .hero-section {
    padding: 60px 24px;
  }
  
  .hero-content h1 {
    font-size: 32px;
    flex-direction: column;
    gap: 12px;
  }
  
  .hero-subtitle {
    font-size: 16px;
  }
  
  section {
    padding: 24px;
  }
  
  section h2 {
    font-size: 20px;
  }
  
  .tech-stacks {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .contact-items {
    gap: 12px;
  }
}
</style>