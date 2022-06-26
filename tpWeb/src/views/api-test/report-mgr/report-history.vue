<template>
  <div class="main" style="padding-left:10px;">
    <!--工具条-->
    <el-col :span="24" class="toolbar" style="padding-bottom: 0;">

      <el-form :inline="true" :model="filters" @submit.native.prevent>
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          align="right"
          unlink-panels
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="yyyy-MM-dd"
          :picker-options="pickerOptions"
          @change="fetchData"
        />
        <el-select v-model="filters.id" placeholder="ID" value-key="id" multiple filterable allow-create clearable @keyup.enter.native="fetchData">
          <el-option v-for="item in []" :key="item.value" :label="item.label" :value="item.value.replace(/[^\d]/g,'')" />
        </el-select>
        <!--        <el-select v-model="filters.env" value-key="id" placeholder="环境筛选" clearable>-->
        <!--          <el-option v-for="item in globalEnv_options" :key="item.id" :label="'环境配置:'+item.name" :value="item" />-->
        <!--        </el-select>-->
        <el-select v-model="filters.build_type" value-key="id" placeholder="构建类型筛选" clearable>
          <el-option v-for="(item, index) in build_type_options" :key="index" :label="item" :value="item" />
        </el-select>
        <!--结果统计维度：用例/步骤-->
        <el-select
          v-model="resultType"
          style="width:100px"
          value-key="id"
          placeholder="请选择结果统计类型"
        >
          <el-option label="用例" value="testcase" />
          <el-option label="步骤" value="teststep" />
        </el-select>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
        </el-form-item>
      </el-form>
    </el-col>

    <!--列表-->
    <el-table
      v-loading="listLoading"
      :data="list"
      highlight-current-row
      :height="tableConfig.height"
      style="width: 100%;"
      :row-class-name="tableRowClassName"
      @selection-change="selsChange"
    >
      <el-table-column v-if="isSuperuser" type="selection" min-width="50" />
      <el-table-column prop="build_status" label="构建状态" min-width="70">
        <template slot-scope="scope">
          <build-status :build-status="scope.row.build_status" :build-result="calculateBuildResultName(scope.row)" />
        </template>
      </el-table-column>
      <el-table-column prop="id" label="ID" min-width="60" sortable />
      <el-table-column prop="create_time" label="时间" min-width="135" sortable />
      <el-table-column prop="env" label="环境" min-width="100" sortable show-overflow-tooltip>
        <template v-if="scope.row.env" slot-scope="scope">
          {{ scope.row.env.name }}({{ scope.row.env.description }})
        </template>
      </el-table-column>
      <el-table-column prop="build_type" label="构建类型" min-width="100" sortable />
      <el-table-column prop="duration" label="耗时（s）" min-width="100" sortable />
      <el-table-column prop="broken_apis" label="阻塞" min-width="70" sortable>
        <template slot-scope="scope">
          <el-button type="text" style="color: #ee0505" @click="handleBrokenApis(scope.row)">
            {{ scope.row.broken_apis.length }}
          </el-button>
        </template>
      </el-table-column>
      <el-table-column v-if="resultType === 'testcase'" label="结果统计（用例）" min-width="500">
        <el-table-column prop="case_pass_rate" label="通过率" min-width="90" sortable>
          <template slot-scope="scope">
            <el-progress
              type="circle"
              :percentage="Math.round(scope.row.case_pass_rate*100)"
              :width="40"
              :color="customColorMethod(Math.round(scope.row.case_pass_rate*100))"
            />
          </template>
        </el-table-column>
        <el-table-column prop="case_total" label="总数" min-width="70" sortable />
        <el-table-column label="通过" min-width="70" sortable>
          <span slot-scope="scope" style="color: #67C23A">{{ scope.row.case_passed }}</span>
        </el-table-column>
        <el-table-column prop="case_failed" label="失败" min-width="70" sortable>
          <!--          <span slot-scope="scope" style="color: #F56C6C">{{ scope.row.case_failed }}</span>-->
          <template slot-scope="scope">
            <el-button type="text" style="color: #ee0505" @click="handleFailed(scope.row, 'case', 'FAILED')">
              {{ scope.row.case_failed }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="case_skipped" label="跳过" min-width="70" sortable>
          <!--          <span slot-scope="scope" style="color: #E6A23C">{{ scope.row.case_skipped }}</span>-->
          <template slot-scope="scope">
            <el-button type="text" style="color: #ee0505" @click="handleFailed(scope.row, 'case', 'SKIPPED')">
              {{ scope.row.case_skipped }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="case_error" label="故障" min-width="70" sortable>
          <span slot-scope="scope" style="color: #F56C6C">{{ scope.row.case_error }}</span>
          <template slot-scope="scope">
            <el-button type="text" style="color: #ee0505" @click="handleFailed(scope.row, 'case', 'ERROR')">
              {{ scope.row.case_error }}
            </el-button>
          </template>
        </el-table-column>
      </el-table-column>
      <el-table-column v-if="resultType === 'teststep'" label="结果统计（测试步骤）" min-width="500">
        <el-table-column prop="step_pass_rate" label="通过率" min-width="90" sortable>
          <template slot-scope="scope">
            <el-progress
              type="circle"
              :percentage="Math.round(scope.row.step_pass_rate*100)"
              :width="40"
              :color="customColorMethod(Math.round(scope.row.step_pass_rate*100))"
            />
          </template>
        </el-table-column>
        <el-table-column prop="step_total" label="总数" min-width="70" sortable />
        <el-table-column label="通过" min-width="70" sortable>
          <span slot-scope="scope" style="color: #67C23A">{{ scope.row.step_passed }}</span>
        </el-table-column>
        <el-table-column prop="step_failed" label="失败" min-width="70" sortable>
          <!--          <span slot-scope="scope" style="color: #F56C6C">{{ scope.row.step_failed }}</span>-->
          <template slot-scope="scope">
            <el-button type="text" style="color: #ee0505" @click="handleFailed(scope.row, 'step', 'FAILED')">
              {{ scope.row.step_failed }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="step_skipped" label="跳过" min-width="70" sortable>
          <!--          <span slot-scope="scope" style="color: #E6A23C">{{ scope.row.step_skipped }}</span>-->
          <template slot-scope="scope">
            <el-button type="text" style="color: #E6A23C" @click="handleFailed(scope.row, 'step', 'SKIPPED')">
              {{ scope.row.step_skipped }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="step_error" label="故障" min-width="70" sortable>
          <!--          <span slot-scope="scope" style="color: #F56C6C">{{ scope.row.step_error }}</span>-->
          <template slot-scope="scope">
            <el-button type="text" style="color: #ee0505" @click="handleFailed(scope.row, 'step', 'ERROR')">
              {{ scope.row.step_error }}
            </el-button>
          </template>
        </el-table-column>
      </el-table-column>
      <el-table-column label="测试报告" min-width="500" sortable>
        <el-table-column prop="Log" label="Log" min-width="70" sortable>
          <template slot-scope="scope">
            <router-link
              target="_blank"
              :to="{ name: 'TestLogs', params: {report_id: scope.row.id}}"
              style="cursor:pointer;color: #0000ff"
            >
              Log
            </router-link>
          </template>
        </el-table-column>
        <el-table-column prop="Report" label="Report" min-width="100" sortable>
          <template slot-scope="scope">
            <el-button
              v-if="scope.row.jenkins_job_name"
              type="text"
              :loading="scope.row.jenkinsAllureUrlLoading"
              @click="handleAllureReport(scope.row)"
            >
              Allure
            </el-button>
            <router-link
              v-if="!scope.row.jenkins_job_name && scope.row.step_total>0"
              :to="{ name: 'PytestHtml', params: {report_id: scope.row.id}}"
              style="cursor:pointer;color: #0000ff"
              target="_blank"
            >
              Pytest
            </router-link>
          </template>
        </el-table-column>
      </el-table-column>
      <el-table-column v-if="isSuperuser" label="操作">
        <template slot-scope="scope">
          <el-button type="danger" @click="handleDel(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!--底部工具条-->
    <el-row class="toolbar">
      <!--分页-->
      <el-col class="pagination-toolbar" :span="24">
        <el-pagination
          background
          style="float:right;"
          :current-page.sync="page"
          layout="total, sizes, prev, pager, next, jumper"
          :page-size="page_size"
          :page-sizes="[20, 50, 100, 1000]"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </el-col>

      <!--批量处理-->
      <el-col v-show="sels.length>0" class="bulk-toolbar" :span="24">
        <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">批量处理: </span>
        <el-button type="danger" plain :disabled="sels.length===0" @click="bulkRemove">删除</el-button>
        <span style="font-size: 14px; padding-right: 30px;"> 选中{{ sels.length }}条</span>
        <el-button type="text" plain @click="sels = []">取消</el-button>
      </el-col>
    </el-row>

    <!--阻塞API列表抽屉页-->
    <el-drawer
      title="阻塞接口列表"
      :with-header="true"
      :wrapper-closable="true"
      :visible.sync="brokenApisFormVisible"
      :append-to-body="true"
      direction="rtl"
      size="65%"
    >
      <div class="demo-drawer__content">
        <el-table :data="broken_apis" style="width: 100%">
          <el-table-column type="expand" width="30">
            <template slot-scope="scope">
              <el-container>
                <el-aside v-loading="baseLoading" element-loading-text="Loading" style="width:40%; padding-left: 5px">
                  <el-divider class="blue-line" direction="vertical" />
                  <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">关联信息</span>
                  <el-form label-position="left" inline class="demo-table-expand" style="padding-bottom: 30px">
                    <el-form-item label="接口ID：">
                      <div v-if="scope.row.api_id">
                        <span style="padding-right: 30px">{{ scope.row.api_id }}</span>
                        <router-link
                          :to="{ name: '接口详情', params: {api_id: scope.row.api_id}}"
                          target="_blank"
                          style="cursor:pointer;color: #0000ff"
                        >
                          <span>接口详情</span>
                        </router-link>
                      </div>
                    </el-form-item>
                    <el-form-item label="用例ID：">
                      <div v-if="scope.row.case_id">
                        <span style="padding-right: 30px">{{ scope.row.case_id }}</span>
                        <router-link
                          :to="{ name: '用例详情', params: {case_id: scope.row.case_id}}"
                          target="_blank"
                          style="cursor:pointer;color: #0000ff"
                        >
                          <span>用例详情</span>
                        </router-link>
                      </div>
                    </el-form-item>
                    <el-form-item label="类型：">
                      <span>{{ scope.row.test_type }}</span>
                    </el-form-item>
                    <el-form-item label="部门：">
                      <span>{{ scope.row.dept_desc }}</span>
                    </el-form-item>
                    <el-form-item label="用例集：">
                      <span>{{ scope.row.suite_desc }}</span>
                    </el-form-item>
                    <el-form-item label="用例：">
                      <span>{{ scope.row.case_desc }}</span>
                    </el-form-item>
                    <el-form-item label="步骤：">
                      <span>{{ scope.row.step_desc }}</span>
                    </el-form-item>
                  </el-form>
                </el-aside>
                <el-main style="padding: 0 10px 0">
                  <el-divider class="blue-line" direction="vertical" />
                  <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">处理结果</span>
                  <el-form label-position="left" inline class="demo-table-expand" style="padding-bottom: 30px">
                    <el-form-item label="BUG：">
                      <span v-if="scope.row.is_bug!==null">{{ scope.row.is_bug?'是':'否' }}</span>
                    </el-form-item>
                    <el-form-item label="描述：">
                      <span style="white-space:pre-wrap;">{{ scope.row.description }}</span>
                    </el-form-item>
                  </el-form>

                </el-main>
              </el-container>
            </template>
          </el-table-column>
          <el-table-column label="序号" type="index" width="50" />
          <el-table-column label="code" prop="rc" sortable show-overflow-tooltip min-width="80">
            <template slot-scope="scope">
              <el-tag type="danger"> {{ scope.row.rc }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="desc" prop="api_desc" show-overflow-tooltip min-width="180">
            <template slot-scope="scope">
              <el-popover
                placement="right"
                width="500"
                trigger="click"
              >
                <el-card class="box-card" shadow="never">
                  <div slot="header" class="clearfix">关联信息</div>
                  <el-form label-position="left" inline class="demo-table-expand">
                    <el-form-item label="接口ID：">
                      <div v-if="scope.row.api_id">
                        <span style="padding-right: 30px">{{ scope.row.api_id }}</span>
                        <router-link
                          :to="{ name: '接口详情', params: {api_id: scope.row.api_id}}"
                          target="_blank"
                          style="cursor:pointer;color: #0000ff"
                        >
                          <span>接口详情</span>
                        </router-link>
                      </div>
                    </el-form-item>
                    <el-form-item label="用例ID：">
                      <div v-if="scope.row.case_id">
                        <span style="padding-right: 30px">{{ scope.row.case_id }}</span>
                        <router-link
                          :to="{ name: '用例详情', params: {case_id: scope.row.case_id}}"
                          target="_blank"
                          style="cursor:pointer;color: #0000ff"
                        >
                          <span>用例详情</span>
                        </router-link>
                      </div>
                    </el-form-item>
                    <el-form-item label="测试类型：">
                      <span>{{ scope.row.test_type }}</span>
                    </el-form-item>
                    <el-form-item label="部门：">
                      <span>{{ scope.row.dept_desc }}</span>
                    </el-form-item>
                    <el-form-item label="用例集：">
                      <span>{{ scope.row.suite_desc }}</span>
                    </el-form-item>
                    <el-form-item label="用例：">
                      <span>{{ scope.row.case_desc }}</span>
                    </el-form-item>
                    <el-form-item label="步骤：">
                      <span>{{ scope.row.step_desc }}</span>
                    </el-form-item>
                  </el-form>
                </el-card>
                <el-button slot="reference" type="text">{{ scope.row.api_desc }}</el-button>
              </el-popover>
            </template>
          </el-table-column>
          <el-table-column label="method" prop="method" sortable show-overflow-tooltip min-width="100" />
          <el-table-column label="url" prop="url" sortable show-overflow-tooltip min-width="300" />
          <el-table-column label="是否BUG" prop="is_bug" sortable min-width="100">
            <template slot-scope="scope">
              <div v-if="scope.row.is_bug!==null">
                <el-tag v-if="scope.row.is_bug===true" type="danger">是</el-tag>
                <el-tag v-if="scope.row.is_bug===false" type="success">否</el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column fixed="right" label="操作" width="60">
            <template slot-scope="scope">
              <!-- v-show="currentRow === scope.row" -->
              <el-row>
                <el-button type="info" icon="el-icon-edit" circle title="编辑" @click="handleEditBrokenApi(scope.$index, scope.row)" />
              </el-row>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-drawer>

    <!--处理阻塞接口抽屉页-->
    <el-drawer
      title="处理阻塞接口"
      :with-header="true"
      :wrapper-closable="true"
      :visible.sync="editBokenApisFormVisible"
      :append-to-body="true"
      direction="rtl"
      size="40%"
    >
      <div class="demo-drawer__content">
        <el-form ref="editBokenApisForm" :model="editBokenApisForm" label-width="120px" :rules="editBokenApisFormRules">
          <el-form-item label="是否BUG" prop="is_bug">
            <el-switch v-model="editBokenApisForm.is_bug" active-color="#ff4949" />
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input v-model="editBokenApisForm.description" type="textarea" :rows="3" />
          </el-form-item>
        </el-form>
        <!-- 取消、提交 -->
        <div class="demo-drawer__footer">
          <el-button @click.native="editBokenApisFormVisible = false;">取消</el-button>
          <el-button type="primary" @click.native="editBokenApisSubmit()">提交</el-button>
        </div>
      </div>
    </el-drawer>

    <!--失败、故障、跳过 列表抽屉页-->
    <el-drawer
      :title="failedFormTitle"
      :with-header="true"
      :wrapper-closable="true"
      :visible.sync="failedFormVisible"
      :append-to-body="true"
      direction="rtl"
      size="65%"
    >
      <div class="demo-drawer__content">
        <el-table :data="failed_list" style="width: 100%">
          <el-table-column type="expand" width="30">
            <template slot-scope="scope">
              <el-container>
                <el-aside v-loading="baseLoading" element-loading-text="Loading" style="width:100%; padding-left: 5px">
                  <el-divider class="blue-line" direction="vertical" />
                  <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">关联信息</span>
                  <el-form label-position="left" inline class="demo-table-expand" style="padding-bottom: 30px">
                    <el-form-item label="用例ID：">
                      <div v-if="scope.row.case_id">
                        <span style="padding-right: 30px">{{ scope.row.case_id }}</span>
                        <router-link
                          :to="{ name: '用例详情', params: {case_id: scope.row.case_id}}"
                          target="_blank"
                          style="cursor:pointer;color: #0000ff"
                        >
                          <span>用例详情</span>
                        </router-link>
                      </div>
                    </el-form-item>
                    <el-form-item label="用例：">
                      <span>{{ scope.row.case_desc }}({{ scope.row.case_name }})</span>
                    </el-form-item>
                    <el-form-item label="步骤：">
                      <span v-if="scope.row.step_id">
                        step{{ scope.row.step_id }}: {{ scope.row.step_name }}
                      </span>
                    </el-form-item>
                    <el-form-item label="步骤描述：">
                      <span v-if="scope.row.step_id">
                        {{ scope.row.step_desc }}
                      </span>
                    </el-form-item>
                  </el-form>
                </el-aside>
              </el-container>
            </template>
          </el-table-column>
          <el-table-column label="序号" type="index" width="50" />
          <el-table-column label="结果" prop="stat" sortable show-overflow-tooltip min-width="80">
            <template slot-scope="scope">
              <el-tag v-if="scope.row.stat==='skipped'" type="warning"> {{ scope.row.stat }}</el-tag>
              <el-tag v-if="scope.row.stat!=='skipped'" type="danger"> {{ scope.row.stat }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="用例" prop="case_name" sortable show-overflow-tooltip min-width="200">
            <template slot-scope="scope">
              <div v-if="scope.row.case_id">
                <router-link
                  :to="{ name: '用例详情', params: {case_id: scope.row.case_id}}"
                  target="_blank"
                  style="cursor:pointer;color: #0000ff"
                >
                  <span>{{ scope.row.case_desc }}</span>
                </router-link>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="步骤" prop="step_name" sortable show-overflow-tooltip min-width="200">
            <template slot-scope="scope">
              <span v-if="scope.row.step_id">
                step{{ scope.row.step_id }}: {{ scope.row.step_name }}
              </span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-drawer>

  </div>
</template>

<script>
import {
  getTestReportList,
  deleteTestReport,
  updateTestReport,
  bulkDeleteTestReport,
  getJenkinsAllure
} from '@/api/api-test/test_report'
// import get_base_data from '@/api/api-test/get_base_data'

import BuildStatus from '@/components/BuildStatus'

export default {
  name: 'ReportHistory',
  components: { BuildStatus },
  // mixins: [get_base_data],
  data() {
    return {
      tableConfig: {
        isLoading: false,
        height: window.innerHeight - 200 // 下面剩余多少空白部分（即最下面距离底部有多少距离）
      },
      build_type_options: [
        '环境验证',
        '冒烟测试',
        '业务巡检',
        '日构建',
        '其他'
      ],
      isSuperuser: false,
      isQaLab: process.env.VUE_APP_BASE_API.indexOf('qalab.companyxyz.com') !== -1,

      dateRange: null,
      filters: {
        id: [],
        env: null
      },
      pickerOptions: {
        shortcuts: [{
          text: '最近一周',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近一个月',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近三个月',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
            picker.$emit('pick', [start, end])
          }
        }]
      },

      // report列表
      list: null,
      total: 0,
      page: 1,
      page_size: 20,
      page_count: 0,
      listLoading: false,
      sels: [], // 列表选中列

      // 阻塞API抽屉页
      brokenApisFormVisible: false,
      broken_apis: [],

      // 失败抽屉页
      failedFormTitle: '',
      failedFormVisible: false,
      failed_list: [],

      // 处理阻塞接口抽屉页
      editBokenApisFormVisible: false,
      editBokenApisFormRules: {},
      editBokenApisForm: {
        index: 0,
        is_bug: false,
        description: ''
      },

      // 结果统计维度：默认为测试步骤
      resultType: 'teststep'
    }
  },
  created() {
  },
  mounted() {
    // this.getEnv()
    this.fetchData()
  },
  methods: {
    // 设置行 颜色
    tableRowClassName({ row }) {
      if (row.status === true) {
        return 'success-row'
      } else {
        return 'error-row'
      }
    },
    // 获取TestReport列表
    fetchData() {
      this.listLoading = true
      const params = {
        page: this.page,
        page_size: this.page_size,
        create_time__gte: this.dateRange ? this.dateRange[0] : this.dateRange,
        create_time__lte: this.dateRange ? this.dateRange[1] : this.dateRange,
        id_in: this.filters.id.join(','),
        env: this.filters.env ? this.filters.env.id : null,
        build_type: this.filters.build_type ? this.filters.build_type : null
      }
      getTestReportList(params).then(response => {
        const { msg, code } = response
        this.listLoading = false
        if (code === 2) {
          this.total = response.data.count
          this.list = response.data.list
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    // 选中行
    selsChange: function(sels) {
      this.sels = sels
    },
    // 刷新每页数据条数
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
      this.page_size = val
      this.fetchData()
    },
    // 刷新指定页数据
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.page = val
      this.fetchData()
    },

    // 删除
    handleDel: function(index, row) {
      this.$confirm('确认删除该记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        this.listLoading = true
        // NProgress.start();
        deleteTestReport(row.id).then(response => {
          const { msg, code } = response
          if (code === 2) {
            this.$message({
              message: '删除成功',
              center: true,
              type: 'success'
            })
          } else {
            this.$message.error({
              message: msg,
              center: true
            })
          }
          this.fetchData()
        })
      })
    },
    // 批量删除
    bulkRemove: function() {
      const ids = this.sels.map(item => item.id)
      this.$confirm('确认删除选中记录吗？', '提示', {
        type: 'warning'
      }).then(() => {
        const params = {
          id_in: ids.join(',')
        }
        bulkDeleteTestReport(params).then(response => {
          const { code, msg } = response
          if (code === 2) {
            this.$message({
              message: '删除成功',
              center: true,
              type: 'success'
            })
          } else {
            this.$message.error({
              message: msg,
              center: true
            })
          }
        }).then(() => { this.fetchData() })
      })
    },
    // 打开Jenkins Allure URL
    openJenkinsAllureURL(jenkinsAllureUrl) {
      if (jenkinsAllureUrl.indexOf('http') !== -1) {
        window.open(jenkinsAllureUrl)
      } else {
        this.$message.warning('报告不存在！jenkins ' + jenkinsAllureUrl)
      }
    },
    // 点击按钮直接打开allure报告
    handleAllureReport(row) {
      this.$set(row, 'jenkinsAllureUrlLoading', true)
      if (!row.allure_url) {
        getJenkinsAllure(row.id, {}).then(response => {
          const { msg, code } = response
          this.$set(row, 'jenkinsAllureUrlLoading', false)
          if (code === 2) {
            this.openJenkinsAllureURL(response.data)
          } else {
            this.$message.error({
              message: msg,
              center: true
            })
          }
        })
      } else {
        this.$set(row, 'jenkinsAllureUrlLoading', false)
        this.openJenkinsAllureURL(row.allure_url)
      }
    },

    // 显示 失败抽屉页
    handleFailed: function(row, type, stat) {
      this.failed_list = []
      if (stat === 'FAILED') {
        if (type === 'case') {
          this.failedFormTitle = '失败用例列表'
          this.failed_list = row.case_failed_list
        } else {
          this.failedFormTitle = '失败步骤列表'
          this.failed_list = row.step_failed_list
        }
      } else if (stat === 'ERROR') {
        if (type === 'case') {
          this.failedFormTitle = '故障用例列表'
          this.failed_list = row.case_error_list
        } else {
          this.failedFormTitle = '故障步骤列表'
          this.failed_list = row.step_error_list
        }
      } else if (stat === 'SKIPPED') {
        if (type === 'case') {
          this.failedFormTitle = '跳过用例列表'
          this.failed_list = row.case_skipped_list
        } else {
          this.failedFormTitle = '跳过步骤列表'
          this.failed_list = row.step_skipped_list
        }
      } else {
        this.failedFormTitle = '空列表'
        this.failed_list = []
      }
      this.failedFormVisible = true
    },

    // 显示 阻塞API抽屉页
    handleBrokenApis: function(row) {
      this.brokenApisFormVisible = true
      this.broken_apis = row.broken_apis
    },
    // 显示 编辑阻塞API抽屉页
    handleEditBrokenApi: function(index, row) {
      this.editBokenApisFormVisible = true
      this.editBokenApisForm = Object.assign({}, row)
      this.editBokenApisForm['index'] = index
    },
    // 编辑 阻塞API
    editBokenApisSubmit: function() {
      this.$refs.editBokenApisForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            // NProgress.start();
            const broken_api_opts = {
              description: this.editBokenApisForm.description,
              is_bug: this.editBokenApisForm.is_bug
            }
            const broken_apis = this.broken_apis
            const broken_api_index = this.editBokenApisForm.index
            broken_apis[broken_api_index] = Object.assign(broken_apis[broken_api_index], broken_api_opts)
            console.log(broken_apis[broken_api_index])
            updateTestReport(this.editBokenApisForm.report_id, { broken_apis: broken_apis }).then(_data => {
              const { msg, code } = _data
              if (code === 2) {
                this.$message({
                  message: '修改成功',
                  center: true,
                  type: 'success'
                })
                this.$refs['editBokenApisForm'].resetFields()
                this.editBokenApisFormVisible = false
                // this.fetchData()
              } else if (code === 400) { // 参数错误或数据库不允许的输入
                this.$message.error({
                  message: msg,
                  center: true
                })
              } else {
                this.$message.error({
                  message: msg,
                  center: true
                })
                this.editBokenApisFormVisible = false
                // this.fetchData()
              }
            })
          })
        }
      })
    },

    // report.broken_apis {code1:[{api1},{api2}]} 转Array[{code:'', method:'', url:'', desc:''}]
    dictKVToArray: function(src) {
      let dst = []
      if (src) {
        for (const code in src) {
          dst = dst.concat(src[code])
        }
      }
      return dst
    },
    // report.broken_apis 字典{code1:[{api1},{api2}]} 计数api个数
    sumDictValuesLength: function(src) {
      let sum = 0
      if (src) {
        const valueArr = Object.values(src)
        for (let i = 0; i < valueArr.length; i++) {
          sum += valueArr[i].length
        }
      }
      return sum
    },
    // validate字典{key:value} 转Array[{key:key, value:value}]
    validateDictKVToArray: function(src) {
      const dst = []
      if (src) {
        for (const k in src) {
          let v = src[k]
          if (typeof v === 'boolean') {
            v = String(v)
          }
          dst.push({ key: k, value: v })
        }
      }
      return dst
    },
    // 自定义颜色
    customColorMethod(percentage) {
      if (percentage < 100) {
        return '#F56C6C'
      } else {
        return '#67C23A'
      }
    },
    // 计算构建类型显示
    calculateBuildResultName: function(row) {
      if (row.step_total === 0) {
        if (row.status === false) {
          return 'last-aborted'
        }
        return 'never-built'
      }
      if (row.status === true) {
        return 'last-successful'
      } else {
        return 'last-failed'
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  ::v-deep .el-drawer__body {
    overflow: auto;
  }
  ::v-deep .demo-drawer__content {
    margin-bottom: 2px;
    padding: 10px 20px 20px;
    overflow: auto;
  }
  ::v-deep .demo-drawer__footer{
    width: 100%;
    position: absolute;
    bottom: 0;
    left: 0;
    border-top: 1px solid #e8e8e8;
    padding: 10px 16px;
    text-align: center;
    background-color: white;
  }
  ::v-deep .el-table .success-row {
    background: #e8fcdf;
  }
  ::v-deep .el-table .error-row {
    background: #f8e1e1;
  }
  ::v-deep .el-table .warning-row {
    background: #fae9c9;
  }

  ::v-deep .demo-table-expand {
    font-size: 0;
  }
  ::v-deep .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
    text-align: right;
  }
  ::v-deep .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
  }
</style>
