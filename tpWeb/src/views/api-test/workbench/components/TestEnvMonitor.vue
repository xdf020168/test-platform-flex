<template>
  <div class="main" style="padding:10px;">
    <!--工具条-->
    <el-col :span="24" class="toolbar">
      <el-form :inline="true" :model="filters" :size="themeSize" @submit.native.prevent>
        <el-form-item>
          <el-input v-model.trim="filters.name" placeholder="名称" clearable @keyup.enter.native="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAdd">新增</el-button>
        </el-form-item>
        <el-form-item>
          <span style="color: #E6A23C">{{ testComments }}</span>
        </el-form-item>
      </el-form>
    </el-col>

    <!--列表-->
    <el-table
      v-loading="tableConfig.isLoading"
      :data="dataList"
      highlight-current-row
      :size="themeSize"
      :height="tableConfig.height"
      style="width: 100%;"
      @selection-change="selsChange"
    >
      <el-table-column type="selection" min-width="50" />
      <el-table-column prop="env" label="环境" sortable show-overflow-tooltip min-width="150">
        <template v-if="scope.row.env" slot-scope="scope">
          <el-popover
            placement="right"
            width="300"
            trigger="click"
          >
            <el-card class="box-card" shadow="never">
              <div slot="header" class="clearfix">
                <span>环境详情</span>
              </div>
              <el-description>
                <el-description-item label="ID" :value="scope.row.env.id" :span="24" :span-map="{md:24}" />
                <el-description-item label="名称" :value="scope.row.env.name" :span="24" :span-map="{md:24}" />
                <el-description-item label="描述" :value="scope.row.env.description" :span="24" :span-map="{md:24}" />
                <el-description-item label="公司" :value="scope.row.env.config.company_id.value" :span="24" :span-map="{md:24}" />
              </el-description>
            </el-card>
            <el-button slot="reference" :size="themeSize" type="text">
              {{ scope.row.env.name }}({{ scope.row.env.description }})
            </el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="validate" label="校验规则" sortable show-overflow-tooltip min-width="150">
        <template slot-scope="scope">
          <el-popover
            placement="right"
            width="500"
            trigger="click"
          >
            <el-card class="box-card" shadow="never">
              <div slot="header" class="clearfix">
                <span>校验规则详情</span>
              </div>
              <el-table :data="validateDictKVToArray(scope.row.validate)" style="width: 100%" :size="themeSize">
                <el-table-column label="key" prop="key" sortable show-overflow-tooltip min-width="150" />
                <el-table-column label="value" prop="value" sortable show-overflow-tooltip min-width="200" />
              </el-table>
            </el-card>
            <el-button slot="reference" :size="themeSize" type="text">
              {{ scope.row.validate.name }}
            </el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column v-if="false" prop="cron" label="定时构建" show-overflow-tooltip min-width="100">
        <template slot-scope="scope">
          <el-popover
            placement="right"
            width="500"
            trigger="click"
          >
            <json-viewer :value="scope.row.cron_job" :expand-depth="2" copyable sort />
            <el-button slot="reference" :size="themeSize" type="text">
              {{ scope.row.cron }}
            </el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="report.create_time" label="上次执行" sortable show-overflow-tooltip min-width="150" />
      <el-table-column prop="report.step_pass_rate" label="通过率" min-width="90" sortable>
        <template slot-scope="scope">
          <el-progress
            type="circle"
            :percentage="scope.row.report?Math.round(scope.row.report.step_pass_rate*100):0"
            :width="40"
            :color="customColorMethod(scope.row.report?Math.round(scope.row.report.step_pass_rate*100):0)"
          />
        </template>
      </el-table-column>
      <el-table-column label="结果统计（测试步骤）" min-width="500">
        <el-table-column prop="report.broken_apis" label="阻塞" min-width="70" sortable>
          <template slot-scope="scope">
            <el-button :size="themeSize" type="text" style="color: #ee0505" @click="handleBrokenApis(scope.row.report)">
              {{ scope.row.report? scope.row.report.broken_apis.length:0 }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="report.step_total" label="总数" min-width="70" sortable>
          <span slot-scope="scope">{{ scope.row.report?scope.row.report.step_total:0 }}</span>
        </el-table-column>
        <el-table-column label="通过" min-width="70" sortable>
          <span slot-scope="scope" style="color: #67C23A">{{ scope.row.report?scope.row.report.step_passed:0 }}</span>
        </el-table-column>
        <el-table-column prop="report.step_failed" label="失败" min-width="70" sortable>
          <!--          <span slot-scope="scope" style="color: #F56C6C">{{ scope.row.report?scope.row.report.step_failed:0 }}</span>-->
          <template slot-scope="scope">
            <el-button :size="themeSize" type="text" style="color: #ee0505" @click="handleFailed(scope.row.report, 'step', 'FAILED')">
              {{ scope.row.report?scope.row.report.step_failed:0 }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="report.step_skipped" label="跳过" min-width="70" sortable>
          <!--          <span slot-scope="scope" style="color: #E6A23C">{{ scope.row.report?scope.row.report.step_skipped:0 }}</span>-->
          <template slot-scope="scope">
            <el-button :size="themeSize" type="text" style="color: #E6A23C" @click="handleFailed(scope.row.report, 'step', 'SKIPPED')">
              {{ scope.row.report?scope.row.report.step_skipped:0 }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="report.step_error" label="故障" min-width="70" sortable>
          <!--          <span slot-scope="scope" style="color: #F56C6C">{{ scope.row.report?scope.row.report.step_error:0 }}</span>-->
          <template slot-scope="scope">
            <el-button :size="themeSize" type="text" style="color: #ee0505" @click="handleFailed(scope.row.report, 'step', 'ERROR')">
              {{ scope.row.report?scope.row.report.step_error:0 }}
            </el-button>
          </template>
        </el-table-column>
      </el-table-column>
      <el-table-column label="测试报告" min-width="500" sortable>
        <el-table-column prop="Log" label="Log" min-width="70" sortable>
          <template slot-scope="scope">
            <router-link
              v-if="scope.row.report"
              target="_blank"
              :to="{ name: 'TestLogs', params: {report_id: scope.row.report.id}}"
              style="cursor:pointer;color: #0000ff"
            >
              Log
            </router-link>
          </template>
        </el-table-column>
        <el-table-column prop="Report" label="Report" min-width="100" sortable>
          <template slot-scope="scope">
            <el-button
              v-if="scope.row.report && scope.row.report.jenkins_job_name"
              type="text"
              :loading="scope.row.report.jenkinsAllureUrlLoading"
              @click="handleAllureReport(scope.row.report)"
            >
              Allure
            </el-button>
            <router-link
              v-if="scope.row.report && !scope.row.report.jenkins_job_name && scope.row.report.step_total>0"
              :to="{ name: 'PytestHtml', params: {report_id: scope.row.report.id}}"
              style="cursor:pointer;color: #0000ff"
              target="_blank"
            >
              Pytest
            </router-link>
          </template>
        </el-table-column>
      </el-table-column>
      <el-table-column fixed="right" label="操作" min-width="150">
        <template slot-scope="scope">
          <el-button type="info" icon="el-icon-edit" circle :size="themeSize" title="编辑" @click="handleEdit(scope.$index, scope.row)" />
          <el-button :loading="scope.row.runLoading" type="primary" icon="el-icon-caret-right" circle :size="themeSize" title="立即执行" @click="handleVerifyEnv(scope.row)" />
          <el-button type="danger" icon="el-icon-delete" circle :size="themeSize" :loading="delLoading" title="删除" @click="handleDel(scope.$index, scope.row)" />
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
        <el-button type="danger" plain :disabled="sels.length===0" :size="themeSize" @click="bulkRemove">删除</el-button>
        <span style="font-size: 14px; padding-right: 30px;"> 选中{{ sels.length }}条</span>
        <el-button type="text" plain :size="themeSize" @click="sels = []">取消</el-button>
      </el-col>
    </el-row>

    <!--编辑界面-->
    <el-drawer
      title="编辑"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="editFormVisible"
      direction="rtl"
      size="50%"
    >
      <div class="demo-drawer__content">
        <el-form ref="editForm" :size="themeSize" :model="editForm" :rules="editFormRules" label-width="160px">
          <el-form-item label="构建类型" prop="build_type">
            <el-input v-model="editForm.build_type" :placeholder="editForm.build_type" :disabled="true" />
          </el-form-item>
          <el-form-item label="测试环境" prop="env">
            <el-select v-model="editForm.env" value-key="id" placeholder="请选择环境配置" style="width:100%" clearable>
              <el-option v-for="item in globalEnv_options" :key="item.id" :label="'环境配置:'+item.name" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="校验规则" prop="validate">
            <el-select v-model="editForm.validate" value-key="id" placeholder="请选择校验规则" style="width:100%" clearable>
              <el-option v-for="item in globalValidate_options" :key="item.id" :label="item.name" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="定时构建" prop="cron">
            <el-input v-model="editForm.cron" placeholder="定时构建cron表达式（TODO）" />
          </el-form-item>
        </el-form>
        <!-- 取消、提交 -->
        <div class="demo-drawer__footer">
          <el-button :size="themeSize" @click.native="editFormVisible = false;editLoading=false">取消</el-button>
          <el-button :size="themeSize" type="primary" :loading="editLoading" @click.native="editSubmit">提交</el-button>
        </div>
      </div>
    </el-drawer>

    <!--新增界面-->
    <el-drawer
      title="新增"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="addFormVisible"
      direction="rtl"
      size="50%"
    >
      <div class="demo-drawer__content">
        <el-form ref="addForm" :size="themeSize" :model="addForm" label-width="160px" :rules="addFormRules">
          <el-form-item label="构建类型" prop="build_type">
            <el-input v-model="addForm.build_type" :placeholder="buildType" :disabled="true" />
          </el-form-item>
          <el-form-item label="测试环境" prop="env">
            <el-select v-model="addForm.env" value-key="id" placeholder="请选择环境配置" style="width:100%" clearable>
              <el-option v-for="item in globalEnv_options" :key="item.id" :label="'环境配置:'+item.name" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="校验规则" prop="validate">
            <el-select v-model="addForm.validate" value-key="id" placeholder="请选择校验规则" style="width:100%" clearable>
              <el-option v-for="item in globalValidate_options" :key="item.id" :label="item.name" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="定时构建" prop="cron">
            <el-input v-model="addForm.cron" placeholder="定时构建cron表达式（TODO）" />
          </el-form-item>
        </el-form>
        <!-- 取消、提交 -->
        <div class="demo-drawer__footer">
          <el-button :size="themeSize" @click.native="addFormVisible = false; addLoading = false">取消</el-button>
          <el-button :size="themeSize" type="primary" :loading="addLoading" @click.native="addSubmit">提交</el-button>
        </div>
      </div>
    </el-drawer>

    <!-- 执行测试-->
    <run-test ref="runTestRef" />

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
        <el-table :data="broken_apis" style="width: 100%" :size="themeSize">
          <el-table-column type="expand" width="30">
            <template slot-scope="scope">
              <el-container>
                <el-aside v-loading="baseLoading" element-loading-text="Loading" style="width:40%; padding-left: 5px">
                  <el-divider class="blue-line" direction="vertical" />
                  <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">关联信息</span>
                  <el-form label-position="left" inline class="demo-table-expand" :size="themeSize" style="padding-bottom: 30px">
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
                  <el-form label-position="left" inline class="demo-table-expand" :size="themeSize" style="padding-bottom: 30px">
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
              <el-tag :size="themeSize" type="danger"> {{ scope.row.rc }}</el-tag>
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
                  <div slot="header" class="clearfix">报告查询</div>
                  <el-form label-position="left" inline class="demo-table-expand" :size="themeSize">
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
                  <!--                  <el-description>-->
                  <!--                    <el-description-item label="用例集" :value="scope.row.suite_desc" :span="24" :span-map="{md:24}" />-->
                  <!--                    <el-description-item label="用例" :value="scope.row.case_desc" :span="24" :span-map="{md:24}" />-->
                  <!--                    <el-description-item label="步骤" :value="scope.row.step_desc" :span="24" :span-map="{md:24}" />-->
                  <!--                  </el-description>-->
                </el-card>
                <el-button slot="reference" :size="themeSize" type="text">{{ scope.row.api_desc }}</el-button>
              </el-popover>
            </template>
          </el-table-column>
          <el-table-column label="method" prop="method" sortable show-overflow-tooltip min-width="100" />
          <el-table-column label="url" prop="url" show-overflow-tooltip min-width="300" />
          <el-table-column label="是否BUG" prop="is_bug" sortable min-width="100">
            <template slot-scope="scope">
              <div v-if="scope.row.is_bug!==null">
                <el-tag v-if="scope.row.is_bug===true" :size="themeSize" type="danger">是</el-tag>
                <el-tag v-if="scope.row.is_bug===false" :size="themeSize" type="success">否</el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column fixed="right" label="操作" width="60">
            <template slot-scope="scope">
              <!-- v-show="currentRow === scope.row" -->
              <el-row>
                <el-button type="info" icon="el-icon-edit" circle :size="themeSize" title="编辑" @click="handleEditBrokenApi(scope.$index, scope.row)" />
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
        <el-form ref="editBokenApisForm" :model="editBokenApisForm" label-width="120px" :size="themeSize" :rules="editBokenApisFormRules">
          <el-form-item label="是否BUG" prop="is_bug">
            <el-switch v-model="editBokenApisForm.is_bug" active-color="#ff4949" />
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input v-model="editBokenApisForm.description" type="textarea" :rows="3" />
          </el-form-item>
        </el-form>
        <!-- 取消、提交 -->
        <div class="demo-drawer__footer">
          <el-button :size="themeSize" @click.native="editBokenApisFormVisible = false;">取消</el-button>
          <el-button :size="themeSize" type="primary" @click.native="editBokenApisSubmit()">提交</el-button>
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
        <el-table :data="failed_list" style="width: 100%" :size="themeSize">
          <el-table-column type="expand" width="30">
            <template slot-scope="scope">
              <el-container>
                <el-aside v-loading="baseLoading" element-loading-text="Loading" style="width:100%; padding-left: 5px">
                  <el-divider class="blue-line" direction="vertical" />
                  <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">关联信息</span>
                  <el-form label-position="left" inline class="demo-table-expand" :size="themeSize" style="padding-bottom: 30px">
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
              <el-tag v-if="scope.row.stat==='skipped'" :size="themeSize" type="warning"> {{ scope.row.stat }}</el-tag>
              <el-tag v-if="scope.row.stat!=='skipped'" :size="themeSize" type="danger"> {{ scope.row.stat }}</el-tag>
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
import JsonViewer from 'vue-json-viewer'
import {
  addTestEnvMonitor, getTestEnvMonitorList, deleteTestEnvMonitor, updateTestEnvMonitor, bulkDeleteTestEnvMonitor
} from '@/api/apiTest/test_env_monitor'
import ElDescription from '@/components/Description/ElDescription'
import ElDescriptionItem from '@/components/Description/ElDescriptionItem'
import ReportHistory from '@/views/api-test/report-mgr/report-history'
import RunTest from '@/views/api-test/components/RunTest'

import get_base_data from '@/api/apiTest/get_base_data'
import { updateTestReport } from '@/api/apiTest/test_report'

export default {
  name: 'EnvValidate',
  components: { JsonViewer, ElDescription, ElDescriptionItem, RunTest },
  mixins: [ReportHistory, get_base_data],
  props: {
    testComments: {
      type: String,
      default() {
        return ''
      }
    },
    buildType: {
      type: String,
      default() {
        return '环境验证'
      }
    }
  },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      tableConfig: {
        isLoading: false,
        height: window.innerHeight - 230 // 下面剩余多少空白部分（即最下面距离底部有多少距离）
      },
      editLoading: false,
      addLoading: false,
      delLoading: false,
      batchDelLoading: false,

      filters: {
        name: ''
      },
      dataList: null,
      total: 0,
      page: 1,
      page_size: 20,
      page_count: 0,
      sels: [], // 列表选中列
      envDefaultConfig: {},

      editFormVisible: false, // 编辑界面是否显示
      // 编辑界面数据规则
      editFormRules: {
        env: [
          { required: true, message: '请选择待测试的环境', trigger: 'blur' }
        ],
        validate: [
          { required: true, message: '请选择校验规则', trigger: 'blur' }
        ]
      },
      // 编辑界面数据
      editForm: {
        env: null,
        validate: null,
        cron: ''
      },

      addFormVisible: false, // 新增界面是否显示
      // 新增界面数据规则
      addFormRules: {
        env: [
          { required: true, message: '请选择待验证环境', trigger: 'blur' }
        ],
        validate: [
          { required: true, message: '请选择校验规则', trigger: 'blur' }
        ]
      },
      // 新增界面数据
      addForm: {
        env: null,
        validate: null,
        cron: ''
      },

      // 批量处理
      bulkEditFormVisible: false,
      bulkEditForm: {
        env: null
      },
      bulkStatus: true,

      // 阻塞API抽屉页
      brokenApisFormVisible: false,
      broken_apis: [],

      // 处理阻塞接口抽屉页
      editBokenApisFormVisible: false,
      editBokenApisFormRules: {},
      editBokenApisForm: {
        index: 0,
        is_bug: false,
        description: ''
      },

      // 失败抽屉页
      failedFormTitle: '',
      failedFormVisible: false,
      failed_list: []
    }
  },
  created() {
  },
  mounted() {
    // this.fetchData()
  },
  methods: {
    // 获取ENV列表
    fetchData() {
      this.tableConfig.isLoading = true
      const params = {
        page: this.page,
        page_size: this.page_size,
        build_type: this.buildType,
        env_name_icontains: this.filters.name
      }
      getTestEnvMonitorList(params).then(response => {
        const { msg, code } = response
        this.tableConfig.isLoading = false
        if (code === 2) {
          this.total = response.data.count
          this.dataList = response.data.list
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
    // 显示编辑界面
    handleEdit: function(index, row) {
      this.getEnv()
      this.getValidate()
      this.editFormVisible = true
      this.editForm = Object.assign({}, row)
    },
    // 显示新增界面
    handleAdd: function() {
      this.getEnv()
      this.getValidate()
      this.addFormVisible = true
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
    // 编辑
    editSubmit: function() {
      this.$refs.editForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.editLoading = true
            // NProgress.start();
            const params = {
              env: this.editForm.env.id,
              validate: this.editForm.validate.id,
              cron: this.editForm.cron,
              report: null
            }
            updateTestEnvMonitor(Number(this.editForm.id), params).then(response => {
              const { msg, code } = response
              this.editLoading = false
              if (code === 2) {
                this.$message({
                  message: '修改成功',
                  center: true,
                  type: 'success'
                })
                this.$refs['editForm'].resetFields()
                this.editFormVisible = false
              } else if (code === 3) {
                this.$message.error({
                  message: msg,
                  center: true
                })
              } else {
                this.$message.error({
                  message: msg,
                  center: true
                })
              }
            }).then(() => {
              this.fetchData()
            })
          })
        }
      })
    },
    // 新增
    addSubmit: function() {
      this.$refs.addForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.addLoading = true
            // NProgress.start();
            const data = {
              env: this.addForm.env.id,
              validate: this.addForm.validate.id,
              cron: this.addForm.cron,
              build_type: this.buildType
            }
            addTestEnvMonitor(data).then(response => {
              const { msg, code } = response
              this.addLoading = false
              if (code === 2) {
                this.$message({
                  message: '添加成功',
                  center: true,
                  type: 'success'
                })
                this.$refs['addForm'].resetFields()
                this.addFormVisible = false
              } else if (code === 3) {
                this.$message.error({
                  message: msg,
                  center: true
                })
              } else {
                this.$message.error({
                  message: msg,
                  center: true
                })
                this.$refs['addForm'].resetFields()
                this.addFormVisible = false
              }
            }).then(() => {
              this.fetchData()
            })
          })
        }
      })
    },
    // 删除
    handleDel: function(index, row) {
      this.$confirm('确认删除该记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        this.delLoading = true
        // NProgress.start();
        deleteTestEnvMonitor(row.id).then(response => {
          const { msg, code } = response
          this.delLoading = false
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
        }).then(() => {
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
        bulkDeleteTestEnvMonitor(params).then(response => {
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
        }).then(() => {
          this.fetchData()
        })
      })
    },
    // 执行验证测试
    handleVerifyEnv: function(row) {
      this.$refs.runTestRef.runForm = {
        golbal_env: row.env,
        golbal_validate: row.validate
      }
      this.$set(row, 'runLoading', true)
      this.$refs.runTestRef.runTestWithFilters('test_case', null, this.buildType).then(() => {
        this.$set(row, 'runLoading', false)
        this.fetchData()
      })
    },

    // 显示 阻塞API抽屉页
    handleBrokenApis: function(row) {
      this.brokenApisFormVisible = true
      this.broken_apis = row ? row.broken_apis : []
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

    // 显示 失败抽屉页
    handleFailed: function(row, type, stat) {
      this.failed_list = []
      if (stat === 'FAILED') {
        if (type === 'case') {
          this.failedFormTitle = '失败用例列表'
          this.failed_list = row ? row.case_failed_list : []
        } else {
          this.failedFormTitle = '失败步骤列表'
          this.failed_list = row ? row.step_failed_list : []
        }
      } else if (stat === 'ERROR') {
        if (type === 'case') {
          this.failedFormTitle = '故障用例列表'
          this.failed_list = row ? row.case_error_list : []
        } else {
          this.failedFormTitle = '故障步骤列表'
          this.failed_list = row ? row.step_error_list : []
        }
      } else if (stat === 'SKIPPED') {
        if (type === 'case') {
          this.failedFormTitle = '跳过用例列表'
          this.failed_list = row ? row.case_skipped_list : []
        } else {
          this.failedFormTitle = '跳过步骤列表'
          this.failed_list = row ? row.step_skipped_list : []
        }
      } else {
        this.failedFormTitle = '空列表'
        this.failed_list = []
      }
      this.failedFormVisible = true
    },

    // 自定义颜色
    customColorMethod(percentage) {
      if (percentage < 100) {
        return '#F56C6C'
      } else {
        return '#67C23A'
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
