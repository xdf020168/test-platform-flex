/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const apiTestRouter = {
  path: '/api_test',
  component: Layout,
  redirect: 'noRedirect',
  name: 'api_test',
  meta: {
    title: '接口测试',
    icon: 'component'
  },
  children: [
    {
      path: 'workbench',
      component: () => import('@/views/charts/mix-chart'),
      name: '工作台',
      meta: { title: '工作台', icon: 'el-icon-s-platform' }
    },
    {
      path: 'globalConfig',
      component: () => import('@/views/charts/mix-chart'),
      name: '全局配置',
      meta: { title: '全局配置', icon: 'el-icon-setting' }
    },
    {
      path: 'apiMgr',
      component: () => import('@/views/charts/mix-chart'),
      name: '接口管理',
      meta: { title: '接口管理' }
    },
    {
      path: 'caseMgr',
      component: () => import('@/views/components-demo/markdown'),
      name: '用例管理',
      meta: { title: '用例管理' }
    },
    {
      path: 'testReport',
      component: () => import('@/views/components-demo/markdown'),
      name: '历史报告',
      meta: { title: '历史报告' }
    },
    {
      path: 'statisticalAnalysis',
      component: () => import('@/views/components-demo/markdown'),
      name: 'api_testcase_management',
      meta: { title: '统计分析' },
      redirect: '/api_test/statisticalAnalysis/summary',
      children: [
        {
          path: 'summary',
          component: () => import('@/views/nested/menu1/menu1-1'),
          name: '概览',
          meta: { title: '概览' }
        },
        {
          path: 'work',
          component: () => import('@/views/nested/menu1/menu1-2'),
          name: '进度分析',
          redirect: '/nested/menu1/menu1-2/menu1-2-1',
          meta: { title: '进度分析' }
        }
      ]
    }
  ]
}

export default apiTestRouter
