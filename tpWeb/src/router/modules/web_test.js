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
      path: 'webCaseMgr',
      component: () => import('@/views/components-demo/markdown'),
      name: 'Web用例管理',
      meta: { title: '用例管理' }
    },
    {
      path: 'webTestReport',
      component: () => import('@/views/components-demo/markdown'),
      name: '测试报告',
      meta: { title: '测试报告' }
    }
  ]
}

export default webTestRouter
