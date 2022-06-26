<template>
  <!-- 构建状态显示 -->
  <span style="width: 40px; height: 40px; " :class="calculateBuildClass(buildResult)">
    <span class="build-status-icon__outer">
      <svg viewBox="0 0 24 24" focusable="false" class="svg-icon ">
        <use v-if="buildStatus==='build-status-static'" href="@/assets/build-status/build-status-sprite.svg#build-status-static" />
        <use v-if="buildStatus==='build-status-in-progress'" href="@/assets/build-status/build-status-sprite.svg#build-status-in-progress" />
      </svg>
    </span>
    <span>
      <svg viewBox="0 0 24 24" focusable="false" class="svg-icon icon-xlg">
        <use v-if="buildResult==='never-built'" href="@/assets/build-status/build-status-sprite.svg#never-built" />
        <use v-if="buildResult==='last-successful'" href="@/assets/build-status/build-status-sprite.svg#last-successful" />
        <use v-if="buildResult==='last-failed'" href="@/assets/build-status/build-status-sprite.svg#last-failed" />
        <use v-if="buildResult==='last-aborted'" href="@/assets/build-status/build-status-sprite.svg#last-aborted" />
      </svg>
    </span>

  </span>
</template>

<script>
export default {
  name: 'BuildStatus',
  props: {
    buildStatus: {
      type: String,
      default() {
        return 'build-status-static'
      }
    },
    buildResult: {
      type: String,
      default() {
        return 'never-built'
      }
    }
  },
  data() {
    return {}
  },
  methods: {
    calculateBuildClass: function(buildResult) {
      switch (buildResult) {
        case 'never-built':
          return 'build-status-icon__wrapper icon-xlg icon-nobuilt'
        case 'last-successful':
          return 'build-status-icon__wrapper icon-xlg icon-blue'
        case 'last-failed':
          return 'build-status-icon__wrapper icon-xlg icon-red'
        default:
          return 'build-status-icon__wrapper icon-xlg icon-disabled'
      }
    }
  }
}
</script>

<style scoped>

</style>
