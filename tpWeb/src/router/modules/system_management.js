/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const systemManagementRouter = {
  path: '/system_management',
  component: Layout,
  redirect: 'noRedirect',
  name: 'system_management',
  meta: {
    title: '系统管理',
    role: ['admin', 'super_editor'],
    icon: 'el-icon-setting'
  },
  children: [
    {
      path: 'organization',
      component: () => import('@/views/components-demo/markdown'),
      name: '团队组织',
      meta: { title: '团队组织', icon: 'peoples' }
    },
    {
      path: 'permission',
      // component: Layout,
      component: () => import('@/views/nested/menu1/index'),
      redirect: '/system_management/permission/page',
      alwaysShow: true, // will always show the root menu
      name: '权限管理',
      meta: {
        title: '权限管理',
        icon: 'lock',
        roles: ['admin', 'editor'] // you can set roles in root nav
      },
      children: [
        {
          path: 'page',
          component: () => import('@/views/permission/page'),
          name: 'PagePermission',
          meta: {
            title: 'Page Permission',
            roles: ['admin'] // or you can only set roles in sub nav
          }
        },
        {
          path: 'directive',
          component: () => import('@/views/permission/directive'),
          name: 'DirectivePermission',
          meta: {
            title: 'Directive Permission'
          // if do not set roles, means: this page does not require permission
          }
        },
        {
          path: 'role',
          component: () => import('@/views/permission/role'),
          name: 'RolePermission',
          meta: {
            title: 'Role Permission',
            roles: ['admin']
          }
        }
      ]
    },
    {
      path: 'theme',
      component: () => import('@/views/components-demo/markdown'),
      name: '主题配置',
      meta: { title: '主题配置', icon: 'theme' }
    },
    {
      path: 'systemLogs',
      component: () => import('@/views/components-demo/markdown'),
      name: '系统日志',
      meta: { title: '系统日志', icon: 'el-icon-notebook-2' }
    }
  ]
}

export default systemManagementRouter
