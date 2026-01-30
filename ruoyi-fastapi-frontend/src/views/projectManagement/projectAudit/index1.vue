<template>
  <div class="app-container">
    <el-tabs v-model="activeTab" type="card" class="mb8">
      <el-tab-pane label="待审核" name="pending" />
      <el-tab-pane label="已审核" name="audited" />
    </el-tabs>

    <el-form
      :model="queryParams"
      ref="queryRef"
      :inline="true"
      v-show="showSearch"
      label-width="90px"
    >
      <el-form-item label="项目名称" prop="projectName">
        <el-input
          v-model="queryParams.projectName"
          placeholder="请输入项目名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="项目类型" prop="projectType">
        <el-input
          v-model="queryParams.projectType"
          placeholder="请输入项目类型"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="审核状态" prop="prefectStatus">
        <el-select
          v-model="queryParams.prefectStatus"
          placeholder="请选择审核状态"
          clearable
          style="width: 240px"
        >
          <el-option
            v-for="item in prefectStatusOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          :disabled="selectedRows.length === 0"
          v-hasPermi="['project:prefect:second-review', 'project:prefect:third-review']"
          @click="handleBatchApprove"
        >批量通过</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          :disabled="selectedRows.length === 0"
          v-hasPermi="['project:prefect:second-review', 'project:prefect:third-review']"
          @click="handleBatchReject"
        >批量拒绝</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="projectList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="项目名称" align="center" prop="projectName" min-width="200">
        <template #default="scope">
          <el-link type="primary" :underline="false" @click="handleOpenDetail(scope.row)">
            {{ scope.row.projectName }}
          </el-link>
        </template>
      </el-table-column>
      <el-table-column label="项目类型" align="center" prop="projectType" min-width="120" />
      <el-table-column label="审核状态" align="center" prop="reviewStatus" min-width="120">
        <template #default="scope">
          <span>{{ getPrefectStatusLabel(scope.row.reviewStatus) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="审核人" align="center" prop="reviewer" min-width="120" />
      <el-table-column label="审核时间" align="center" prop="reviewTime" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.reviewTime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width" width="160">
        <template #default="scope">
          <el-button
            link
            type="primary"
            @click="handleApprove(scope.row)"
            :disabled="!canApprove(scope.row)"
            v-hasPermi="['project:prefect:second-review', 'project:prefect:third-review']"
          >通过</el-button>
          <el-button
            link
            type="danger"
            @click="handleReject(scope.row)"
            :disabled="!canReject(scope.row)"
            v-hasPermi="['project:prefect:second-review', 'project:prefect:third-review']"
          >拒绝</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total > 0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />
  </div>
</template>

<script setup name="ProjectAudit">
import { listProject, secondReviewProject, secondReviewProjectBatch, thirdReviewProject, thirdReviewProjectBatch } from "@/api/project/projects";
import { useRouter } from "vue-router";
import { parseTime } from "@/utils/ruoyi";

const { proxy } = getCurrentInstance();
const router = useRouter();

const loading = ref(true);
const showSearch = ref(true);
const total = ref(0);
const projectList = ref([]);

const activeTab = ref("pending");
const selectedRows = ref([]);

const prefectStatusOptions = [
  { value: "01", label: "创建" },
  { value: "02", label: "工程师修改" },
  { value: "03", label: "二级复审" },
  { value: "04", label: "三级复审" },
  { value: "05", label: "待归档" },
  { value: "06", label: "已归档" }
];

const prefectStatusLabelMap = prefectStatusOptions.reduce((acc, cur) => {
  acc[cur.value] = cur.label;
  return acc;
}, {});

const queryParams = ref({
  pageNum: 1,
  pageSize: 10,
  projectName: undefined,
  projectType: undefined,
  prefectStatus: undefined
});

function getPrefectStatusLabel(value) {
  if (!value) return "-";
  return prefectStatusLabelMap[value] || value;
}

function canApprove(row) {
  if (!row) return false;
  return row.reviewStatus === "03" || row.reviewStatus === "04";
}

function canReject(row) {
  if (!row) return false;
  return row.reviewStatus === "03" || row.reviewStatus === "04";
}

function getTabDefaultStatus() {
  if (activeTab.value === "pending") return "03,04";
  return "01,02,05,06";
}

async function getList() {
  loading.value = true;
  try {
    const params = {
      ...queryParams.value,
      prefectStatus: queryParams.value.prefectStatus || getTabDefaultStatus()
    };
    const res = await listProject(params);
    const rows = res?.data?.rows || [];
    total.value = res?.data?.total || 0;
    projectList.value = rows.map(r => ({
      ...r,
      reviewStatus: r.reviewStatus || r.prefectStatus,
      reviewer: r.reviewer || r.operatorName,
      reviewTime: r.reviewTime || r.updateTime
    }));
  } finally {
    loading.value = false;
  }
}

function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

function resetQuery() {
  proxy.resetForm("queryRef");
  queryParams.value.pageNum = 1;
  getList();
}

function handleSelectionChange(selection) {
  selectedRows.value = Array.isArray(selection) ? selection : [];
}

function handleOpenDetail(row) {
  if (!row) return;
  router.push({
    path: "/projectManagement/projectInfo/detail",
    query: { id: row.proId, type: "view" }
  });
}

async function handleApprove(row) {
  if (!row || !canApprove(row)) return;
  try {
    const { value } = await proxy.$modal.prompt(`请输入通过意见（项目：${row.projectName}）`);
    if (!value || !String(value).trim()) {
      proxy.$modal.msgError("请填写审核意见");
      return;
    }
    await proxy.$modal.confirm(`确认通过项目“${row.projectName}”吗？`);
    if (row.reviewStatus === "03") {
      await secondReviewProject({ proId: row.proId, currentStatus: "03", targetStatus: "04", opinionContent: value });
    } else if (row.reviewStatus === "04") {
      await thirdReviewProject({ proId: row.proId, currentStatus: "04", targetStatus: "05", opinionContent: value });
    }
    proxy.$modal.msgSuccess("操作成功");
    getList();
  } catch (e) {}
}

async function handleReject(row) {
  if (!row || !canReject(row)) return;
  try {
    const { value } = await proxy.$modal.prompt(`请输入拒绝意见（项目：${row.projectName}）`);
    if (!value || !String(value).trim()) {
      proxy.$modal.msgError("请填写审核意见");
      return;
    }
    await proxy.$modal.confirm(`确认拒绝项目“${row.projectName}”吗？`);
    if (row.reviewStatus === "03") {
      await secondReviewProject({ proId: row.proId, currentStatus: "03", targetStatus: "02", opinionContent: value });
    } else if (row.reviewStatus === "04") {
      await thirdReviewProject({ proId: row.proId, currentStatus: "04", targetStatus: "02", opinionContent: value });
    }
    proxy.$modal.msgSuccess("操作成功");
    getList();
  } catch (e) {}
}

async function handleBatchApprove() {
  const rows = selectedRows.value.filter(r => canApprove(r));
  if (!rows.length) {
    proxy.$modal.msgError("所选数据均不可通过");
    return;
  }
  try {
    const { value } = await proxy.$modal.prompt(`请输入批量通过意见（${rows.length}条）`);
    if (!value || !String(value).trim()) {
      proxy.$modal.msgError("请填写审核意见");
      return;
    }
    await proxy.$modal.confirm(`确认批量通过 ${rows.length} 条数据吗？`);
    const secondRows = rows.filter(r => r.reviewStatus === "03");
    const thirdRows = rows.filter(r => r.reviewStatus === "04");
    const tasks = [];
    if (secondRows.length) {
      tasks.push(
        secondReviewProjectBatch({
          proIds: secondRows.map(r => r.proId),
          currentStatus: "03",
          targetStatus: "04",
          opinionContent: value
        })
      );
    }
    if (thirdRows.length) {
      tasks.push(
        thirdReviewProjectBatch({
          proIds: thirdRows.map(r => r.proId),
          currentStatus: "04",
          targetStatus: "05",
          opinionContent: value
        })
      );
    }
    if (!tasks.length) {
      proxy.$modal.msgError("所选数据均不可通过");
      return;
    }
    await Promise.all(tasks);
    proxy.$modal.msgSuccess("操作成功");
    selectedRows.value = [];
    getList();
  } catch (e) {}
}

async function handleBatchReject() {
  const rows = selectedRows.value.filter(r => canReject(r));
  if (!rows.length) {
    proxy.$modal.msgError("所选数据均不可拒绝");
    return;
  }
  try {
    const { value } = await proxy.$modal.prompt(`请输入批量拒绝意见（${rows.length}条）`);
    if (!value || !String(value).trim()) {
      proxy.$modal.msgError("请填写审核意见");
      return;
    }
    await proxy.$modal.confirm(`确认批量拒绝 ${rows.length} 条数据吗？`);
    const secondRows = rows.filter(r => r.reviewStatus === "03");
    const thirdRows = rows.filter(r => r.reviewStatus === "04");
    const tasks = [];
    if (secondRows.length) {
      tasks.push(
        secondReviewProjectBatch({
          proIds: secondRows.map(r => r.proId),
          currentStatus: "03",
          targetStatus: "02",
          opinionContent: value
        })
      );
    }
    if (thirdRows.length) {
      tasks.push(
        thirdReviewProjectBatch({
          proIds: thirdRows.map(r => r.proId),
          currentStatus: "04",
          targetStatus: "02",
          opinionContent: value
        })
      );
    }
    if (!tasks.length) {
      proxy.$modal.msgError("所选数据均不可拒绝");
      return;
    }
    await Promise.all(tasks);
    proxy.$modal.msgSuccess("操作成功");
    selectedRows.value = [];
    getList();
  } catch (e) {}
}

watch(activeTab, () => {
  queryParams.value.pageNum = 1;
  getList();
});

getList();
</script>
