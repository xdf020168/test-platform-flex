<template>
  <test-env-monitor :test-comments="comments" :build-type="build_type" />
</template>

<script>
import TestEnvMonitor from '@/views/api-test/workbench/components/TestEnvMonitor'
export default {
  name: 'EnvSmoke',
  components: { TestEnvMonitor },
  data() {
    return {
      comments: '注：默认执行 = 单接口用例（P0） + 场景用例',
      build_type: '冒烟测试'
    }
  }
}
</script>

<style scoped>

</style>
