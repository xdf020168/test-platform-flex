// const fa = require("element-ui/src/locale/lang/fa");
module.exports = {
  title: 'TestPlatformFlex',

  /**
   * @type {boolean} true | false
   * @description Whether show the settings right-panel
   * 页面设置侧边显示
   */
  showSettings: false,

  /**
   * @type {boolean} true | false
   * @description Whether need tagsView
   * 页面标签
   */
  tagsView: false,

  /**
   * @type {boolean} true | false
   * @description Whether fix the header
   */
  fixedHeader: false,

  /**
   * @type {boolean} true | false
   * @description Whether show the logo in sidebar
   */
  sidebarLogo: false,

  /**
   * @type {string | array} 'production' | ['production', 'development']
   * @description Need show err logs component.
   * The default is only used in the production env
   * If you want to also use it in dev, you can pass ['production', 'development']
   */
  errorLog: 'production'
}
