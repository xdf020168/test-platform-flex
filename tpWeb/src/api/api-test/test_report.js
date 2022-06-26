import request from '@/utils/request'

// 获取测试报告列表
export function getTestReportList(params) {
  return request({
    url: '/api/api_test/test/report/list',
    method: 'get',
    params: params
  })
}

// 获取测试报告详情
export function getTestReportDetail(pk, params) {
  return request({
    url: '/api/api_test/test/report/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 局部更新用例步骤
export function updateTestReport(pk, data) {
  return request({
    url: '/api/api_test/test/report/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量局部更新用例步骤
export function bulkUpdateTestReport(dataArr) {
  return request({
    url: '/api/api_test/test/report/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除测试报告
export function deleteTestReport(pk) {
  return request({
    url: '/api/api_test/test/report/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除测试报告
export function bulkDeleteTestReport(params) {
  return request({
    url: '/api/api_test/test/report/bulk/',
    method: 'delete',
    params
  })
}

// 测试报告 - pytest-html
export function getPytestHtml(pk, params) {
  return request({
    url: '/api/api_test/test/report/pytest_html/' + pk + '/',
    method: 'get',
    params
  })
}

// 测试报告 - Jenkins Allure
export function getJenkinsAllure(pk, params) {
  return request({
    url: '/api/api_test/test/report/jenkins_allure/' + pk + '/',
    method: 'get',
    params
  })
}

// 测试报告 - test logs
export function getTestLogs(pk, params) {
  return request({
    url: '/api/api_test/test/report/logs/' + pk + '/',
    method: 'get',
    params
  })
}
