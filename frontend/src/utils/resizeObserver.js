/**
 * ResizeObserver 工具类
 * 解决 ResizeObserver loop completed with undelivered notifications 错误
 */

class SafeResizeObserver {
  constructor(callback) {
    this.callback = callback
    this.observer = null
    this.observedElements = new Set()
    this.pendingCallbacks = new Map()
    this.rafId = null
    
    this.init()
  }
  
  init() {
    if (!window.ResizeObserver) {
      console.warn('ResizeObserver is not supported in this browser')
      return
    }
    
    this.observer = new ResizeObserver((entries, observer) => {
      // 使用 requestAnimationFrame 来延迟执行，避免循环
      if (this.rafId) {
        cancelAnimationFrame(this.rafId)
      }
      
      this.rafId = requestAnimationFrame(() => {
        try {
          this.callback(entries, observer)
        } catch (error) {
          // 忽略 ResizeObserver 相关的错误
          if (!error.message.includes('ResizeObserver')) {
            console.error('ResizeObserver callback error:', error)
          }
        }
        this.rafId = null
      })
    })
  }
  
  observe(element, options) {
    if (!this.observer) return
    
    try {
      this.observer.observe(element, options)
      this.observedElements.add(element)
    } catch (error) {
      console.error('Failed to observe element:', error)
    }
  }
  
  unobserve(element) {
    if (!this.observer) return
    
    try {
      this.observer.unobserve(element)
      this.observedElements.delete(element)
    } catch (error) {
      console.error('Failed to unobserve element:', error)
    }
  }
  
  disconnect() {
    if (!this.observer) return
    
    try {
      this.observer.disconnect()
      this.observedElements.clear()
      
      if (this.rafId) {
        cancelAnimationFrame(this.rafId)
        this.rafId = null
      }
    } catch (error) {
      console.error('Failed to disconnect ResizeObserver:', error)
    }
  }
  
  // 获取当前观察的元素数量
  getObservedCount() {
    return this.observedElements.size
  }
}

// 创建全局的 ResizeObserver 错误处理器
export function setupResizeObserverErrorHandler() {
  // 忽略 ResizeObserver 的常见警告
  const originalConsoleError = console.error
  
  console.error = (...args) => {
    const message = args[0]
    if (typeof message === 'string') {
      if (message.includes('ResizeObserver loop completed with undelivered notifications') ||
          message.includes('ResizeObserver loop limit exceeded')) {
        return // 忽略这些警告
      }
    }
    originalConsoleError.apply(console, args)
  }
  
  // 全局错误处理
  window.addEventListener('error', (e) => {
    if (e.message && e.message.includes('ResizeObserver')) {
      e.preventDefault()
      return false
    }
  })
  
  // 未处理的 Promise 拒绝
  window.addEventListener('unhandledrejection', (e) => {
    if (e.reason && e.reason.message && e.reason.message.includes('ResizeObserver')) {
      e.preventDefault()
      return false
    }
  })
}

// 创建安全的 ResizeObserver 实例
export function createSafeResizeObserver(callback) {
  return new SafeResizeObserver(callback)
}

// 默认导出
export default SafeResizeObserver
