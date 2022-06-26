<template>
  <div class="main">
    <!--  标签页  -->
    <el-tabs v-model="activeName" :tab-position="tabPosition" @tab-click="clickTab">
      <el-tab-pane
        v-for="(item,index) in tabPaneList"
        :key="index"
        :label="item.label"
        :name="item.name"
        lazy
      >
        <component :is="component" v-for="(component,idx) in item.components" :key="idx" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  name: '',
  props: {
    tabPaneList: {
      type: Array,
      default() {
        return []
      }
    },
    tabPosition: {
      type: String,
      default() {
        return 'top'
      }
    }
  },
  data() {
    return {
      activeName: '' // 默认选中
    }
  },
  created() {
    this.getMenuList()
  },
  mounted() {
  },
  methods: {
    // 获取标签页列表
    getMenuList() {
      if (this.tabPaneList.length > 0) {
        this.activeName = this.tabPaneList[0].name
      }
    },
    // 控制每次点击标签，都重新请求子组件的接口
    clickTab(tab, event) {
      // console.log(tab, event)
    }
  }
}
</script>

<style lang="scss" scoped>
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
  ::v-deep .el-tabs__item.is-active {
    color: #047AE2;
    font-weight: 700;
  }
  ::v-deep .el-tabs__active-bar {
    height: 4px;
    position: absolute;
    bottom: 0;
    left: 0;
    z-index: 1;
    list-style: none;
  }
  ::v-deep .el-tabs--left .el-tabs__item.is-left {
    text-align: center;
  }
</style>
