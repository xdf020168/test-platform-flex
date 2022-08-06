<template>
  <tabs-menu :tab-pane-list="tabPaneList" />
</template>

<script>
import TabsMenu from '@/components/TabsMenu'
import EnvSmoke from '@/views/api-test/workbench/env-smoke'
import EnvValidate from '@/views/api-test/workbench/env-validate'

export default {
  name: 'Workbench',
  components: { TabsMenu },
  data() {
    return {
      tabPaneList: [
        // {
        //   name: 'jobBoard',
        //   label: '工作看板',
        //   components: [jobBoard]
        // },
        // {
        //   name: 'FastTest',
        //   label: '快速测试',
        //   components: [FastTest]
        // },
        // {
        //   name: 'EnvInspection',
        //   label: '业务巡检',
        //   components: [EnvInspection]
        // },
        {
          name: 'EnvSmoke',
          label: '冒烟测试',
          components: [EnvSmoke]
        },
        {
          name: 'EnvValidate',
          label: '环境验证',
          components: [EnvValidate]
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>
