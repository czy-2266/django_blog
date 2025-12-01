/**
 * API响应处理工具函数
 */

/**
 * 处理Django REST Framework的分页响应格式
 * @param {*} response - API响应数据
 * @returns {Array} 处理后的数组数据
 */
export function handlePaginatedResponse(response) {
  if (Array.isArray(response)) {
    return response
  }
  
  // 处理Django REST Framework的分页格式
  if (response && response.results) {
    return response.results
  }
  
  // 处理其他可能的格式
  if (response && Array.isArray(response.data)) {
    return response.data
  }
  
  // 如果都不是，返回空数组
  return []
}

/**
 * 安全地过滤数组数据
 * @param {Array} data - 要过滤的数据
 * @param {Function} filterFn - 过滤函数，默认为过滤掉null和undefined
 * @returns {Array} 过滤后的数组
 */
export function safeFilter(data, filterFn = (item) => item != null) {
  if (!Array.isArray(data)) {
    return []
  }
  return data.filter(filterFn)
}

/**
 * 处理分类API响应
 * @param {*} response - 分类API响应
 * @returns {Array} 处理后的分类数组
 */
export function handleCategoriesResponse(response) {
  const categories = handlePaginatedResponse(response)
  return safeFilter(categories, (category) => category != null && category.id)
}

/**
 * 处理文章API响应
 * @param {*} response - 文章API响应
 * @returns {Array} 处理后的文章数组
 */
export function handleArticlesResponse(response) {
  const articles = handlePaginatedResponse(response)
  return safeFilter(articles, (article) => article != null && article.id)
}
