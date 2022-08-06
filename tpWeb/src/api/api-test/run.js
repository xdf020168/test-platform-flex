import request from '@/utils/request'

// 测试执行 - 指定数据
export function testRun(data) {
  return request({
    url: '/api/api_test/test/run/',
    method: 'post',
    data: data
  })
}

// 测试执行 - 指定筛选条件
export function testRunWithFilters(data) {
  return request({
    url: '/api/api_test/test/run_with_filters/',
    method: 'post',
    data: data
  })
}
