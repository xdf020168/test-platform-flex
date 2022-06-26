<template>
  <div class="main">
    <div v-loading="isLoading">
      <p style="padding-left: 10px;white-space: pre-wrap;" v-text="logContent" />
    </div>
  </div>
</template>

<script>
import { getTestLogs } from '@/api/api-test/test_report'

export default {
  name: 'PytestHtmlReport',
  data() {
    return {
      isLoading: false,
      logContent: ''
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.isLoading = true
      getTestLogs(this.$route.params.report_id, {}).then(response => {
        const { msg, code } = response
        this.isLoading = false
        if (code === 2) {
          this.logContent = response.data
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
