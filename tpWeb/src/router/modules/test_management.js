/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const testManagementRouter = {
  path: '/test_management',
  component: Layout,
  redirect: 'noRedirect',
  name: 'test_management',
  meta: {
    title: '测试管理',
    icon: 'component'
  },
  children: [
    {
      path: 'statistics',
      component: () => import('@/views/dashboard/index'),
      name: 'statistics',
      meta: { title: '统计分析', icon: 'chart' }
    },
    {
      path: 'bugs',
      component: () => import('@/views/table/inline-edit-table'),
      name: 'bugs',
      meta: { title: 'BUG列表', icon: 'bug' }
    }
  ]
}

export default testManagementRouter
