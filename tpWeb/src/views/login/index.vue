<template>
  <el-container class="login-container">
    <el-header>
      <el-row>
        <el-col :span="24">
          <div class="page-title">自动化测试平台</div>
        </el-col>
      </el-row>
    </el-header>
    <el-main style="padding: 0">
      <el-row>
        <el-col :span="6">
          <div class="bottom-left">
            <img src="~@/assets/login_images/bottom-left.png" alt="">
          </div>
        </el-col>
        <el-col :span="24" style="padding-top: 140px">
          <el-card class="login-register-card">
            <el-tabs v-model="activeName">
              <el-tab-pane label="登录" name="login">
                <el-radio v-model="loginType" label="normal">普通登录</el-radio>
                <el-radio v-model="loginType" label="ldap">LDAP登录</el-radio>
                <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left">
                  <el-form-item prop="username">
                    <span class="svg-container">
                      <svg-icon icon-class="user" />
                    </span>
                    <el-input
                      ref="username"
                      v-model="loginForm.username"
                      placeholder="Username"
                      name="username"
                      type="text"
                      tabindex="1"
                      auto-complete="on"
                    />
                  </el-form-item>

                  <el-form-item prop="password">
                    <span class="svg-container">
                      <svg-icon icon-class="password" />
                    </span>
                    <el-input
                      :key="passwordType"
                      ref="password"
                      v-model="loginForm.password"
                      :type="passwordType"
                      placeholder="Password"
                      name="password"
                      tabindex="2"
                      auto-complete="on"
                      @keyup.enter.native="handleLogin"
                    />
                    <span class="show-pwd" @click="showPwd">
                      <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
                    </span>
                  </el-form-item>

                  <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;" @click.native.prevent="handleLogin">Login</el-button>

                  <div class="tips">
                    <span style="margin-right:20px;">username: user</span>
                    <span> password: any</span>
                  </div>
                  <div>
                    <social-sign />
                  </div>

                </el-form>
              </el-tab-pane>
              <el-tab-pane label="注册" name="third">TODO</el-tab-pane>
            </el-tabs>
          </el-card>
        </el-col>
        <el-col :span="6">
          <div v-if="false" class="bottom-right">
            <img src="~@/assets/login_images/bottom-right.png" alt="">
          </div>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import { validUsername } from '@/utils/validate'
import SocialSign from './components/SocialSignin'

export default {
  name: 'Login',
  components: { SocialSign },
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!validUsername(value)) {
        callback(new Error('Please enter the correct user name'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('The password can not be less than 6 digits'))
      } else {
        callback()
      }
    }
    return {
      activeName: 'login', // tabs 默认标签页
      loginType: 'normal',
      loginForm: {
        username: 'admin',
        password: 'Pass@0301'
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/login', this.loginForm).then(() => {
            this.$router.push({ path: this.redirect || '/' })
            this.loading = false
          }).catch(() => {
            this.loading = false
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#acccea;
$light_gray:#fff;
$cursor: #000000; //基础黑色
$dark_primary: #303133;  //主要文字
$dark_normal: #606266; //常规文字
$light_blue: #acccea; //浅蓝色

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $dark_primary;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $dark_primary !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
//$bg:#FFFFFF;
$bg:#FFFFFF;
$dark_gray:#889aa4;
$light_gray:#eee;

$dark_primary: #303133;  //主要文字
$dark_normal: #606266; //常规文字
$light_blue: #acccea; //浅蓝色

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .page-title {
    font-size: 40px;
    text-align: center;
    margin-top: 80px;
  }
  .bottom-right {
    position: fixed;
    right: 0;
    bottom: 0;
  }
  .bottom-left {
    position: fixed;
    left: 0;
    bottom: 0;
  }
  .bottom-right img {
    width: 464px;
    height: 308px;
  }
  .bottom-left img {
    width: 500px;
    height: 300px;
  }
  .login-register-card {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 0 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }
  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 20px 0 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #67C23A;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 20px;
      color: $light_gray;
      margin: 0px auto 20px auto;
      text-align: left;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}

  ::v-deep .el-tabs__item.is-active {
    color: #047AE2;
    font-weight: 700;
  }
  ::v-deep .el-tabs__item {
    box-sizing: border-box;
    height: 35px;
    color: #2c4068;
    margin: 0;
    text-align: center;
    overflow: hidden!important;
    text-overflow: ellipsis;
    white-space: nowrap;
    word-break: break-all;
    font-weight: 400;
    min-width: 100px;
    font-size: 14px;
    line-height: 22px;
    padding: 9px 0;
    position: relative;
    display: inline-block;
    list-style: none;
  }
  ::v-deep .el-tabs__active-bar {
    height: 4px;
    position: absolute;
    bottom: 0;
    left: 0;
    z-index: 1;
    list-style: none;
  }
  ::v-deep .el-tabs__header .el-tabs__bar {
    border: none;
  }
</style>
