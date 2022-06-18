/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const webTestRouter = {
  path: '/web_test',
  component: Layout,
  redirect: 'noRedirect',
  name: 'web_test',
  meta: {
    title: 'Web测试',
    icon: 'component'
  },
  children: [
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

export default webTestRouter
