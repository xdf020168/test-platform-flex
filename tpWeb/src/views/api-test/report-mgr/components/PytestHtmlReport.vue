<template>
  <div class="main">
    <div v-loading="isLoading">
      <p style="padding-left: 10px" v-html="htmlContent" />
    </div>
  </div>
</template>

<script>
import { getPytestHtml } from '@/api/api-test/test_report'

export default {
  name: 'PytestHtmlReport',
  data() {
    return {
      isLoading: false,
      htmlContent: ''
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.isLoading = true
      getPytestHtml(this.$route.params.report_id, {}).then(response => {
        const { msg, code } = response
        this.isLoading = false
        if (code === 2) {
          this.htmlContent = response.data
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
