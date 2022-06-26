import request from '@/utils/request'

export function login(data) {
  return request({
    // url: '/vue-element-admin/user/login',
    url: '/api/user_auth/jwt/token/v2',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    // url: '/vue-element-admin/user/info',
    url: '/api/user_auth/jwt/token/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/api/user_auth/jwt/user/logout',
    method: 'post'
  })
}
