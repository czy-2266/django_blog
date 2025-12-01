const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,

  // 生产环境优化
  productionSourceMap: false,

  // 开发服务器配置
  devServer: {
    port: 8085,
    host: '0.0.0.0',
    allowedHosts: 'all',
    client: {
      overlay: {
        errors: true,
        warnings: false
      }
    },
    // 配置代理解决跨域问题
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8002',
        changeOrigin: true,
        secure: false,
        logLevel: 'debug'
      }
    }
  },

  // 构建优化
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            chunks: 'all',
          },
          elementPlus: {
            test: /[\\/]node_modules[\\/]element-plus[\\/]/,
            name: 'element-plus',
            chunks: 'all',
          }
        }
      }
    }
  },

  // PWA配置
  pwa: {
    name: 'Ice BLOG',
    themeColor: '#87CEEB',
    msTileColor: '#87CEEB',
    manifestOptions: {
      background_color: '#ffffff'
    }
  },

  // CSS优化
  css: {
    extract: true,
    sourceMap: false,
    loaderOptions: {
      sass: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    }
  }
})