/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const dataFactoryRouter = {
  path: '/data_factory',
  component: Layout,
  redirect: 'noRedirect',
  name: 'data_factory',
  meta: {
    title: '数据工厂',
    icon: 'component'
  },
  children: [
    {
      path: 'dataMgr',
      component: () => import('@/views/components-demo/markdown'),
      name: '数据生成器',
      meta: { title: '数据生成器' }
    },
    {
      path: 'dataMgr',
      component: () => import('@/views/components-demo/markdown'),
      name: '数据生成器2',
      meta: { title: '数据生成器2' }
    }
  ]
}

export default dataFactoryRouter
