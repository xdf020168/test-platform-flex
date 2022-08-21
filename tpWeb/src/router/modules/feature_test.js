/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const featureTestRouter = {
  path: '/feature_test',
  component: Layout,
  redirect: 'noRedirect',
  name: 'feature_test',
  meta: {
    title: 'Web测试',
    icon: 'component'
  },
  children: [
    {
      path: 'featureCaseMgr',
      component: () => import('@/views/components-demo/markdown'),
      name: '用例管理',
      meta: { title: '用例管理' }
    },
    {
      path: 'featureTestReport',
      component: () => import('@/views/components-demo/markdown'),
      name: '测试报告',
      meta: { title: '测试报告' }
    }
  ]
}

export default featureTestRouter
