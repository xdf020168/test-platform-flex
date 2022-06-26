/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const performanceTestRouter = {
  path: '/perf_test',
  component: Layout,
  redirect: 'noRedirect',
  name: 'perf_test',
  meta: {
    title: '性能测试',
    icon: 'component'
  },
  children: [
    {
      path: 'dataMgr',
      component: () => import('@/views/components-demo/markdown'),
      name: '数据管理2',
      meta: { title: '数据管理2' }
    },
    {
      path: 'testPerfReport',
      component: () => import('@/views/components-demo/markdown'),
      name: '性能报告',
      meta: { title: '历史报告' }
    }
  ]
}

export default performanceTestRouter
