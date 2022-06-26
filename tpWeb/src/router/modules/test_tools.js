/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const testToolsRouter = {
  path: '/test_tools',
  component: Layout,
  redirect: 'noRedirect',
  name: 'test_tools',
  meta: {
    title: '测试工具',
    icon: 'component'
  },
  children: [
    {
      path: 'envValidate',
      component: () => import('@/views/components-demo/markdown'),
      name: '环境验证',
      meta: { title: '环境验证' }
    },
    {
      path: 'coreReplace',
      component: () => import('@/views/components-demo/markdown'),
      name: 'core替换',
      meta: { title: 'core替换' }
    }
  ]
}

export default testToolsRouter
