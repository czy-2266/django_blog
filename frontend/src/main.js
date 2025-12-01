import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './styles/element-theme.css'
import { Palette as ElPaletteIcon } from '@element-plus/icons-vue'

const app = createApp(App)
const pinia = createPinia()

// 简化的 ResizeObserver 错误处理
const originalConsoleError = console.error
console.error = (...args) => {
  const message = args[0]
  if (typeof message === 'string' && message.includes('ResizeObserver')) {
    return // 忽略 ResizeObserver 错误
  }
  originalConsoleError.apply(console, args)
}

app.use(pinia)
app.use(ElementPlus)

// ✅ 注册图标
app.component('ElPaletteIcon', ElPaletteIcon)

app.use(router)
app.mount('#app')