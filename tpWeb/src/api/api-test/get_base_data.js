import { getGlobalEnvList } from '@/api/apiTest/global_env'
import { getGlobalHeaderList } from '@/api/apiTest/global_header'
import { getGlobalLabelList } from '@/api/apiTest/global_label'
import { getUserList } from '@/api/apiTest/user'
import { getProjectList } from '@/api/apiTest/project'
import { getDepartmentList } from '@/api/apiTest/department'
import { getTestSuiteList } from '@/api/apiTest/test_suite'
import { getApiInfoList } from '@/api/apiTest/api_info'
import { getApiGroupList } from '@/api/apiTest/api_group'
import { getTestCaseList } from '@/api/apiTest/test_case'
import { getGlobalResponseValidateList } from '@/api/apiTest/global_response_validate'

export default {
  data() {
    return {
      baseLoading: false,
      // 获取公共数据，--供表单选择
      user_options: [], // 用户列表
      department_options: [], // 部门列表
      project_options: [], // 项目列表
      deptProjectTreeData: [], // 部门-项目 Tree

      globalEnv_options: [], // 全局环境配置
      globalHeader_options: [], // 全局Header配置
      globalLabel_options: [], // 全局标签
      globalValidate_options: [], // 全局校验规则
      defaultGlobalValidate: null, // mor全局校验规则

      api_group_options: [], // 接口分组
      apiInfo_options: [], // 接口
      deptProjectApiGroupTreeData: [], // 部门-项目-接口分组 Tree
      deptProjectApiGroupApiTreeData: [], // 部门-项目-接口分组-接口 Tree

      test_suite_options: [], // 用例集
      test_case_options: [], // 用例
      deptSuiteTreeData: [], // 部门-用例集 Tree
      deptSuiteCaseTreeData: [], // 部门-用例集-用例 Tree

      // 部门-接口 tree data
      deptApiTreeProps: {
        label: 'label',
        children: 'children',
        isLeaf: 'isLeaf'
      },
      // 部门-用例 tree data
      deptCaseTreeProps: {
        label: 'label',
        children: 'children',
        isLeaf: 'isLeaf'
      },

      // 统计数据
      noCaseApiCountByProject: []
    }
  },
  methods: {
    // 获取User、全局Env、Header、Label
    getUser() {
      if (this.user_options.length > 0) {
        return
      }
      this.baseLoading = true
      getUserList({}).then((res) => {
        const { msg, code } = res
        this.baseLoading = false
        if (code === 2) {
          this.user_options = res.data.list
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    getEnv() {
      if (this.globalEnv_options.length > 0) {
        return
      }
      this.baseLoading = true
      getGlobalEnvList({}).then(response => {
        const { msg, code } = response
        this.baseLoading = false
        if (code === 2) {
          this.globalEnv_options = response.data.list
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    getHeader() {
      if (this.globalHeader_options.length > 0) {
        return
      }
      this.baseLoading = true
      getGlobalHeaderList({}).then(response => {
        const { msg, code } = response
        this.baseLoading = false
        if (code === 2) {
          this.globalHeader_options = response.data.list
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    getLabel(label_type_names = null) {
      if (this.globalLabel_options.length > 0) {
        return
      }
      const globalLabel_options = []
      this.baseLoading = true
      getGlobalLabelList({ status: true }).then(response => {
        const { msg, code } = response
        this.baseLoading = false
        if (code === 2) {
          const labels = response.data.list
          for (let i = 0; i < labels.length; i++) {
            const lb = labels[i]
            let match_label = false
            for (let j = 0; j < globalLabel_options.length; j++) {
              if (globalLabel_options[j].label === lb.type_name) {
                globalLabel_options[j].options.push(lb)
                match_label = true
                break
              }
            }
            if (!match_label) {
              if (!label_type_names || label_type_names.indexOf(lb.type_name) !== -1) {
                globalLabel_options.push({ label: lb.type_name, options: [lb] })
              }
            }
          }
          this.globalLabel_options = globalLabel_options
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    getValidate() {
      if (this.globalValidate_options.length > 0) {
        return
      }
      this.baseLoading = true
      getGlobalResponseValidateList({}).then(response => {
        const { msg, code } = response
        this.baseLoading = false
        if (code === 2) {
          this.globalValidate_options = response.data.list
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    getDefaultValidate() {
      this.baseLoading = true
      return getGlobalResponseValidateList({ is_default: true }).then(response => {
        const { msg, code } = response
        this.baseLoading = false
        if (code === 2 && response.data.list.length > 0) {
          this.defaultGlobalValidate = response.data.list[0]
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },

    // 查询 部门列表
    getDepartment() {
      if (this.department_options.length > 0) {
        return
      }
      this.baseLoading = true
      return getDepartmentList({}).then(response => {
        this.department_options = response.data.list
        this.baseLoading = false
      })
    },
    // 查询 项目列表
    getProject() {
      if (this.project_options.length > 0) {
        return
      }
      this.baseLoading = true
      return getProjectList({}).then(response => {
        this.project_options = response.data.list
        this.baseLoading = false
      })
    },

    // 查询 接口分组
    getApiGroup(project_id = '') {
      if (this.api_group_options.length > 0) {
        return
      }
      this.baseLoading = true
      return getApiGroupList({ project: project_id }).then((res) => {
        const { msg, code } = res
        this.baseLoading = false
        if (code === 2) {
          this.api_group_options = res.data.list
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    // 查询 接口列表...
    getApiInfo() {
      if (this.apiInfo_options.length > 0) {
        return
      }
      this.baseLoading = true
      return getApiInfoList({}).then((res) => {
        const { msg, code } = res
        this.baseLoading = false
        if (code === 2) {
          this.apiInfo_options = res.data.list
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },

    // 查询 用例集列表
    getTestSuite() {
      if (this.test_suite_options.length > 0) {
        return
      }
      this.baseLoading = true
      return getTestSuiteList({}).then((res) => {
        const { msg, code } = res
        this.baseLoading = false
        if (code === 2) {
          this.test_suite_options = res.data.list
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    // 查询 用例列表
    getTestCase() {
      if (this.test_case_options.length > 0) {
        return
      }
      this.baseLoading = true
      return getTestCaseList({}).then((res) => {
        const { msg, code } = res
        this.baseLoading = false
        if (code === 2) {
          this.test_case_options = res.data.list
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },

    // ============== Tree Load ==============
    // 部门树 Lv0
    deptTreeLoad(node, resolve, leaf = false, menu = true, defaultLv0 = []) {
      const dataLv0 = menu ? defaultLv0 : []
      this.baseLoading = true
      getDepartmentList({ page_size: 100 }).then(response => {
        this.department_options = response.data.list
        const deptList = response.data.list
        for (let i = 0; i < deptList.length; i++) {
          const dept = deptList[i]
          dataLv0.push({
            label: dept.name,
            isLeaf: leaf,
            leaf: leaf,
            type: 'department',
            id: dept.id,
            value: { id: dept.id, name: dept.name },
            children: []
          })
        }
      }).then(() => {
        this.baseLoading = false
        return resolve(dataLv0)
      })
    },

    // 项目树 Lv1
    projectTreeLoad(node, resolve, leaf = false) {
      const dataLv1 = []
      getProjectList({ page_size: 1000, department: node.data.id }).then(response => {
        this.project_options = response.data.list
        const projectList = response.data.list
        for (let i = 0; i < projectList.length; i++) {
          const project = projectList[i]
          dataLv1.push({
            label: project.name,
            isLeaf: leaf,
            leaf: leaf,
            type: 'project',
            id: project.id,
            value: { id: project.id, name: project.name },
            children: []
          })
        }
      }).then(() => { return resolve(dataLv1) })
    },

    // 获取 部门-项目 Tree
    deptProjectTreeLoad(node, resolve) {
      const leaf = node.level >= 1
      // 部门
      if (node.level === 0) {
        const defaultLv0 = [
          { label: '全部项目', isLeaf: true, type: 'allProject' },
          { label: '待分配项目', isLeaf: true, type: 'toDoProject' }
        ]
        this.deptTreeLoad(node, resolve, leaf, true, defaultLv0)
      }
      // 项目
      if (node.level === 1) {
        this.projectTreeLoad(node, resolve, leaf)
      }
    },

    // 获取 部门-项目-接口分组-接口 Tree
    deptApiTreeLoad(node, resolve, max_level = 3, menu = true) {
      // label | isLeaf | children  -- el-tree
      // label | leaf | children | value -- el-cascader
      // type | id 自定义
      const leaf = node.level >= max_level
      // 部门
      if (node.level === 0) {
        const defaultLv0 = [
          { label: '全部接口', isLeaf: true, type: 'allApi' },
          { label: '全部分组', isLeaf: true, type: 'allGroup' },
          { label: '待分配接口', isLeaf: true, type: 'toAllocateApi' }
        ]
        this.deptTreeLoad(node, resolve, leaf, menu, defaultLv0)
      }
      // 项目
      if (node.level === 1) {
        this.projectTreeLoad(node, resolve, leaf)
      }
      // 接口分组
      if (node.level === 2) {
        const dataLv2 = []
        getApiGroupList({ page_size: 1000, project: node.data.id }).then(response => {
          this.api_group_options = response.data.list
          const apiGroupList = response.data.list
          for (let i = 0; i < apiGroupList.length; i++) {
            const apiGroup = apiGroupList[i]
            dataLv2.push({
              label: apiGroup.name,
              isLeaf: leaf,
              leaf: leaf,
              type: 'api_group',
              id: apiGroup.id,
              value: { id: apiGroup.id, name: apiGroup.name },
              children: []
            })
          }
        }).then(() => { return resolve(dataLv2) })
      }
      // 接口
      if (node.level === 3) {
        const dataLv3 = []
        getApiInfoList({ page_size: 1000, api_group: node.data.id }).then(response => {
          this.apiInfo_options = response.data.list
          const apiList = response.data.list
          for (let i = 0; i < apiList.length; i++) {
            const api = apiList[i]
            dataLv3.push({
              label: api.name,
              isLeaf: leaf,
              leaf: leaf,
              type: 'api',
              id: api.id,
              value: api,
              children: []
            })
          }
        }).then(() => { return resolve(dataLv3) })
      }
    },

    // 获取 部门-用例集-用例 Tree
    deptCaseTreeLoad(node, resolve, max_level = 2, menu = true, filter = null) {
      // label | isLeaf | children  -- el-tree
      // label | leaf | children | value -- el-cascader
      // type | id 自定义

      // 参数 filter示例：
      // {"test_suite": {"labels": ["P0"]}, "test_case": {"type": "setup"}}

      const leaf = node.level >= max_level
      // 部门
      if (node.level === 0) {
        const defaultLv0 = [
          { label: '全部用例', isLeaf: true, type: 'allCase' },
          { label: '全部步骤', isLeaf: true, type: 'allStep' },
          { label: '全部用例集', isLeaf: true, type: 'allSuite' },
          { label: '待分配用例集', isLeaf: true, type: 'toDoSuite' }
        ]
        this.deptTreeLoad(node, resolve, leaf, menu, defaultLv0)
      }
      // 用例集
      if (node.level === 1) {
        const dataLv1 = []
        let params = { page_size: 1000, department: node.data.id }
        if (filter && filter.test_suite) {
          params = Object.assign(params, filter.test_suite)
        }
        getTestSuiteList(params).then(response => {
          this.test_suite_options = response.data.list
          const suiteList = response.data.list
          for (let i = 0; i < suiteList.length; i++) {
            const suite = suiteList[i]
            dataLv1.push({
              label: suite.name,
              isLeaf: leaf,
              leaf: leaf,
              type: 'suite',
              id: suite.id,
              value: { id: suite.id, name: suite.name },
              children: []
            })
          }
        }).then(() => { return resolve(dataLv1) })
      }
      // 用例
      if (node.level === 2) {
        const dataLv2 = []
        let params = { page_size: 1000, test_suite: node.data.id }
        if (filter && filter.test_case) {
          params = Object.assign(params, filter.test_case)
        }
        getTestCaseList(params).then(response => {
          this.test_case_options = response.data.list
          const caseList = response.data.list
          for (let i = 0; i < caseList.length; i++) {
            const testCase = caseList[i]
            dataLv2.push({
              label: testCase.name,
              isLeaf: leaf,
              leaf: leaf,
              type: 'case',
              id: testCase.id,
              value: { id: testCase.id, name: testCase.name },
              children: []
            })
          }
        }).then(() => { return resolve(dataLv2) })
      }
    }
  }
}
