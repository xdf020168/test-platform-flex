<template>
  <div class="main">
    <!-- 执行测试->选择环境配置->确认-->
    <el-dialog
      title="执行-选择环境配置"
      :visible.sync="runFormVisible"
      :close-on-click-modal="false"
      :append-to-body="true"
      style="width: 75%; left: 12.5%"
    >
      <el-form ref="runForm" :model="runForm" :size="themeSize" label-width="100px" :rules="runFormRules">
        <el-form-item label="环境配置" prop="golbal_env">
          <el-select v-model="runForm.golbal_env" value-key="id" placeholder="请选择环境配置" style="width:100%" clearable>
            <el-option v-for="item in globalEnv_options" :key="item.id" :label="'环境配置:'+item.name" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="校验规则" prop="golbal_validate">
          <el-select v-model="runForm.golbal_validate" value-key="id" placeholder="请选择校验规则" style="width:100%" clearable>
            <el-option v-for="item in globalValidate_options" :key="item.id" :label="item.name" :value="item" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button :size="themeSize" @click.native="runFormVisible = false">取消</el-button>
        <el-button :size="themeSize" type="primary" @click.native="runTest(runForm.level, runForm.rows)">确定</el-button>
      </div>
    </el-dialog>
  </div>

</template>

<script>
import { testRun } from '@/api/api-test/run'
import get_base_data from '@/api/api-test/get_base_data'

export default {
  name: 'RunTest',
  mixins: [get_base_data],
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      // 执行用例步骤
      batchRunLoading: false, // 批量执行按钮loading
      runFormVisible: false,
      runFormRules: {
        golbal_env: [{ required: true, message: '请输入选择环境配置', trigger: 'blur' }],
        golbal_validate: [{ required: true, message: '请输入选择校验规则', trigger: 'blur' }]
      },
      runForm: {
        golbal_env: null, // 执行时选择 环境配置
        golbal_validate: '', // 执行时选择 校验规则
        level: null, // 执行时选择 测试数据类型：test_suite / test_case / test_step
        rows: [] // 待执测试数据列表
      },

      // 告警
      alertData: {
        title: '',
        type: 'success',
        message: ''
      }
    }
  },
  mounted() {
    // this.getEnv()
  },
  methods: {
    fetchData() {
      this.getEnv()
      this.getValidate()
      this.getDefaultValidate().then(() => { this.runForm.golbal_validate = this.defaultGlobalValidate })
    },
    handleRunTest: function(level, rows) {
      this.fetchData()
      this.runForm.level = level
      this.runForm.rows = rows
      this.runFormVisible = true
    },
    // 运行用例步骤
    runTest: function(level, rows, filters = null, build_type = '其他') {
      this.$refs.runForm.validate((valid) => {
        if (valid) {
          this.runFormVisible = false

          if (rows.length === 0) {
            this.$message.warning({ message: '无可执行测试！' })
            return true
          } else if (rows.length === 1) {
            this.$set(rows[0], 'runLoading', true)
          } else {
            this.batchRunLoading = true
          }
          const data = {
            'level': level,
            'list': rows,
            'filters': filters,
            'build_type': build_type,
            'env': this.runForm.golbal_env,
            'validate': this.runForm.golbal_validate
          }
          testRun(data).then(response => {
            const { data, code, msg, success } = response
            let status = false
            let failed = 0
            let error = 0
            if (Object.prototype.hasOwnProperty.call(data, 'status')) {
              status = data['status']
            }
            if (Object.prototype.hasOwnProperty.call(data, 'failed')) {
              failed = data['failed']
            }
            if (Object.prototype.hasOwnProperty.call(data, 'error')) {
              error = data['error']
            }

            if (success === 'true') {
              if ((failed + error) === 0 && status === true) {
                this.alertData.type = 'success'
              } else {
                this.alertData.type = 'error'
              }
              this.alertData.message = Object.keys(data).map(k => `${k}: ${String(data[k])}</br>`).join('')
            } else {
              this.alertData.message = data.replace(/\r\n/g, '<br>').replace(/\n/g, '<br>')
              this.alertData.type = 'warning'
            }
            this.alertData.title = msg
            if (code === 2) {
              this.$alert(this.alertData.message, {
                type: this.alertData.type,
                title: msg,
                showClose: true,
                closeOnPressEscape: true,
                lockScroll: true,
                dangerouslyUseHTMLString: true,
                customClass: this.alertData.type === 'warning' ? 'my-message-box' : ''
              })
            } else {
              this.$message.error({
                message: msg,
                center: true,
                duration: 30000
              })
            }
            this.$set(rows[0], 'runLoading', false)
            this.batchRunLoading = false
          })
        }
      })
    },
    runTestWithFilters: function(level, filters, build_type = '其他') {
      const data = {
        'level': level,
        'list': 'all',
        'filters': filters,
        'build_type': build_type,
        'env': this.runForm.golbal_env,
        'validate': this.runForm.golbal_validate
      }
      return testRun(data).then(response => {
        const { data, code, msg, success } = response
        let status = false
        let failed = 0
        let error = 0
        if (Object.prototype.hasOwnProperty.call(data, 'status')) {
          status = data['status']
        }
        if (Object.prototype.hasOwnProperty.call(data, 'failed')) {
          failed = data['failed']
        }
        if (Object.prototype.hasOwnProperty.call(data, 'error')) {
          error = data['error']
        }

        if (success === 'true') {
          if ((failed + error) === 0 && status === true) {
            this.alertData.type = 'success'
          } else {
            this.alertData.type = 'error'
          }
          this.alertData.message = Object.keys(data).map(k => `${k}: ${String(data[k])}</br>`).join('')
        } else {
          this.alertData.message = data.replace(/\r\n/g, '<br>').replace(/\n/g, '<br>')
          this.alertData.type = 'warning'
        }
        this.alertData.title = msg
        if (code === 2) {
          this.$alert(this.alertData.message, {
            type: this.alertData.type,
            title: msg,
            showClose: true,
            closeOnPressEscape: true,
            lockScroll: true,
            dangerouslyUseHTMLString: true,
            customClass: this.alertData.type === 'warning' ? 'my-message-box' : ''
          })
        } else {
          this.$message.error({
            message: msg,
            center: true,
            duration: 30000
          })
        }
      })
    }
  }
}
</script>

<style>
  .el-message-box__wrapper {
    overflow: auto;
  }
  .my-message-box {
    word-break: break-all !important;
    overflow: auto;
    width: 60%;
  }
</style>
