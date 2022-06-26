<template>
  <div class="main">
    todo
  </div>
</template>

<script>
import { getJenkinsAllure } from '@/api/api-test/test_report'

export default {
  name: 'AllureHtmlReport',
  data() {
    return {
      isLoading: false,
      jenkinsAllureUrl: ''
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.isLoading = true
      getJenkinsAllure(this.$route.params.report_id, {}).then(response => {
        const { msg, code } = response
        this.isLoading = false
        if (code === 2) {
          this.jenkinsAllureUrl = response.data
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
