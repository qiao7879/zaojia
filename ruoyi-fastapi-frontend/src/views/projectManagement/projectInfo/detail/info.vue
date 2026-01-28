<template>
  <div class="app-container">
    <el-card class="mb8">
      <template #header>
        <div class="page-header">
          <div class="page-title">
            <div class="title">
              {{ projectInfo.projectName || "项目详情" }}
            </div>
            <div class="sub">
              <el-tag size="small" :type="prefectTagType">
                {{ prefectStatusLabel }}
              </el-tag>
              <span class="sub-item">项目编码：{{ projectInfo.projectCode || "-" }}</span>
              <span class="sub-item">项目类型：{{ projectInfo.projectType || "-" }}</span>
            </div>
          </div>
          <div class="page-actions">
            <el-button icon="ArrowLeft" @click="goBack">返回</el-button>
            <el-button type="primary" icon="Edit" @click="toggleEdit">
              {{ editMode ? "取消编辑" : "编辑" }}
            </el-button>
            <el-button v-if="editMode" type="success" icon="Check" :loading="saving" @click="saveProject">
              保存
            </el-button>
          </div>
        </div>
      </template>
      <el-steps :active="currentStep" finish-status="success" align-center>
        <el-step v-for="item in stepItems" :key="item.value" :title="item.title" />
      </el-steps>
    </el-card>

    <el-row :gutter="12">
      <el-col :xs="24" :lg="16">
        <el-card>
          <template #header>
            <span class="card-title">基本信息</span>
          </template>

          <el-descriptions v-if="!editMode" :column="2" border>
            <el-descriptions-item label="项目编码" :label-width="110">
              {{ projectInfo.projectCode || "-" }}
            </el-descriptions-item>
            <el-descriptions-item label="项目全称" :label-width="110">
              {{ projectInfo.projectName || "-" }}
            </el-descriptions-item>
            <el-descriptions-item label="业主单位" :label-width="110">
              {{ projectInfo.entName || "-" }}
            </el-descriptions-item>
            <el-descriptions-item label="使用单位" :label-width="110">
              {{ projectInfo.userCompany || "-" }}
            </el-descriptions-item>
            <el-descriptions-item label="服务内容" :label-width="110">
              {{ projectInfo.serviceContent || "-" }}
            </el-descriptions-item>
            <el-descriptions-item label="负责人" :label-width="110">
              {{ projectInfo.projectManager || "-" }}
            </el-descriptions-item>
            <el-descriptions-item label="项目成员" :label-width="110">
              {{ projectInfo.coordinator || "-" }}
            </el-descriptions-item>
            <el-descriptions-item label="项目开始时间" :label-width="110">
              {{ parseTime(projectInfo.startDate, "{y}-{m}-{d}") || "-" }}
            </el-descriptions-item>
            <el-descriptions-item label="项目预计结束时间" :label-width="110">
              {{ parseTime(projectInfo.endDate, "{y}-{m}-{d}") || "-" }}
            </el-descriptions-item>
            <el-descriptions-item label="项目状态" :label-width="110">
              {{ projectInfo.status || "-" }}
            </el-descriptions-item>
            <el-descriptions-item label="备注" :label-width="110" :span="2">
              {{ projectInfo.remarks || "-" }}
            </el-descriptions-item>
          </el-descriptions>

          <el-form v-else :model="projectInfo" label-width="110px">
            <el-row :gutter="12">
              <el-col :xs="24" :sm="12">
                <el-form-item label="项目编码">
                  <el-input v-model="projectInfo.projectCode" disabled />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="项目全称">
                  <el-input v-model="projectInfo.projectName" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="项目类型">
                  <el-input v-model="projectInfo.projectType" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="业主单位">
                  <el-input v-model="projectInfo.entName" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="使用单位">
                  <el-input v-model="projectInfo.userCompany" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="服务内容">
                  <el-input v-model="projectInfo.serviceContent" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="负责人">
                  <el-input v-model="projectInfo.projectManager" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="项目成员">
                  <el-input v-model="projectInfo.coordinator" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="开始时间">
                  <el-date-picker v-model="projectInfo.startDate" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="预计结束时间">
                  <el-date-picker v-model="projectInfo.endDate" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :xs="24">
                <el-form-item label="备注">
                  <el-input v-model="projectInfo.remarks" type="textarea" :rows="2" />
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </el-card>

        <el-card class="mt12">
          <template #header>
            <span class="card-title">业务信息</span>
          </template>

          <el-tabs v-model="activeTab" type="card">
            <el-tab-pane label="合同" name="contract">
              <el-descriptions v-if="!editMode" :column="2" border>
                <el-descriptions-item label="合同签订状态" :label-width="110">
                  {{ projectInfo.contractSigned || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="是否已取得文件" :label-width="110">
                  {{ projectInfo.documentObtained || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="合同折扣说明" :label-width="110">
                  {{ projectInfo.contractDiscount || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="合同金额" :label-width="110">
                  {{ projectInfo.contractAmount ?? "-" }}
                </el-descriptions-item>
              </el-descriptions>
              <el-form v-else :model="projectInfo" label-width="110px">
                <el-row :gutter="12">
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="合同签订状态">
                      <el-input v-model="projectInfo.contractSigned" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="是否已取得文件">
                      <el-input v-model="projectInfo.documentObtained" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24">
                    <el-form-item label="合同折扣说明">
                      <el-input v-model="projectInfo.contractDiscount" />
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-form>
            </el-tab-pane>

            <el-tab-pane label="开票与回款" name="invoice">
              <el-descriptions v-if="!editMode" :column="2" border>
                <el-descriptions-item label="应开票金额" :label-width="110">
                  {{ projectInfo.invoiceShouldAmount ?? "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="已开票金额" :label-width="110">
                  {{ projectInfo.invoiceIssuedAmount ?? "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="剩余可开票金额" :label-width="110">
                  {{ projectInfo.invoiceRemainingAmount ?? "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="是否已开具发票" :label-width="110">
                  {{ projectInfo.invoiceIssued || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="发票开具日期" :label-width="110">
                  {{ parseTime(projectInfo.invoiceDate, "{y}-{m}-{d}") || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="是否已申请付款" :label-width="110">
                  {{ projectInfo.paymentApplied || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="请款月份" :label-width="110">
                  {{ parseTime(projectInfo.paymentMonth, "{y}-{m}-{d}") || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="业主是否已回款" :label-width="110">
                  {{ projectInfo.paymentReceived || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="已回款金额" :label-width="110">
                  {{ projectInfo.paymentReceivedAmount ?? "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="回款到账日期" :label-width="110">
                  {{ parseTime(projectInfo.paymentReceivedDate, "{y}-{m}-{d}") || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="剩余未回款金额" :label-width="110">
                  {{ projectInfo.paymentRemainingAmount ?? "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="项目回款率" :label-width="110">
                  {{ projectInfo.paymentRecoveryRate ?? "-" }}
                </el-descriptions-item>
              </el-descriptions>

              <el-form v-else :model="projectInfo" label-width="110px">
                <el-row :gutter="12">
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="应开票金额">
                      <el-input v-model="projectInfo.invoiceShouldAmount" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="已开票金额">
                      <el-input v-model="projectInfo.invoiceIssuedAmount" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="是否已开具发票">
                      <el-input v-model="projectInfo.invoiceIssued" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="发票开具日期">
                      <el-date-picker v-model="projectInfo.invoiceDate" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="是否已申请付款">
                      <el-input v-model="projectInfo.paymentApplied" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="请款月份">
                      <el-date-picker v-model="projectInfo.paymentMonth" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="业主是否已回款">
                      <el-input v-model="projectInfo.paymentReceived" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="已回款金额">
                      <el-input v-model="projectInfo.paymentReceivedAmount" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="回款到账日期">
                      <el-date-picker v-model="projectInfo.paymentReceivedDate" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="项目回款率">
                      <el-input v-model="projectInfo.paymentRecoveryRate" />
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-form>
            </el-tab-pane>

            <el-tab-pane label="对账与提成" name="recon">
              <el-descriptions v-if="!editMode" :column="2" border>
                <el-descriptions-item label="是否已对账" :label-width="110">
                  {{ projectInfo.reconciliationDone || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="双方对账日期" :label-width="110">
                  {{ parseTime(projectInfo.reconciliationDate, "{y}-{m}-{d}") || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="对账凭证" :label-width="110">
                  {{ projectInfo.reconciliationVoucher || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="是否已计提提成" :label-width="110">
                  {{ projectInfo.commissionAccrued || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="提成金额" :label-width="110">
                  {{ projectInfo.commissionAmount ?? "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="提成计提日期" :label-width="110">
                  {{ parseTime(projectInfo.commissionDate, "{y}-{m}-{d}") || "-" }}
                </el-descriptions-item>
              </el-descriptions>
              <el-form v-else :model="projectInfo" label-width="110px">
                <el-row :gutter="12">
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="是否已对账">
                      <el-input v-model="projectInfo.reconciliationDone" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="双方对账日期">
                      <el-date-picker v-model="projectInfo.reconciliationDate" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="对账凭证">
                      <el-input v-model="projectInfo.reconciliationVoucher" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="是否已计提提成">
                      <el-input v-model="projectInfo.commissionAccrued" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="提成金额">
                      <el-input v-model="projectInfo.commissionAmount" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="提成计提日期">
                      <el-date-picker v-model="projectInfo.commissionDate" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-form>
            </el-tab-pane>

            <el-tab-pane label="存档" name="archive">
              <el-descriptions v-if="!editMode" :column="2" border>
                <el-descriptions-item label="合同电子档已存档" :label-width="110">
                  {{ projectInfo.contractElectronicSaved || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="合同文件编号" :label-width="110">
                  {{ projectInfo.contractFile || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="成果电子档已存档" :label-width="110">
                  {{ projectInfo.deliverableElectronicSaved || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="成果文件编号" :label-width="110">
                  {{ projectInfo.deliverableFile || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="纸质资料存档情况" :label-width="110">
                  {{ projectInfo.documentPaperSaved || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="资料存档类型说明" :label-width="110">
                  {{ projectInfo.documentSaveType || "-" }}
                </el-descriptions-item>
              </el-descriptions>
              <el-form v-else :model="projectInfo" label-width="110px">
                <el-row :gutter="12">
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="合同电子档已存档">
                      <el-input v-model="projectInfo.contractElectronicSaved" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="合同文件编号">
                      <el-input v-model="projectInfo.contractFile" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="成果电子档已存档">
                      <el-input v-model="projectInfo.deliverableElectronicSaved" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="成果文件编号">
                      <el-input v-model="projectInfo.deliverableFile" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="纸质资料存档情况">
                      <el-input v-model="projectInfo.documentPaperSaved" />
                    </el-form-item>
                  </el-col>
                  <el-col :xs="24" :sm="12">
                    <el-form-item label="资料存档类型说明">
                      <el-input v-model="projectInfo.documentSaveType" />
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="8">
        <el-card>
          <template #header>
            <span class="card-title">流程与意见</span>
          </template>

          <el-descriptions :column="1" border size="small">
            <el-descriptions-item label="当前节点" :label-width="110">
              {{ prefectStatusLabel }}
            </el-descriptions-item>
            <el-descriptions-item label="审核人" :label-width="110">
              {{ prefectInfo.operatorName || "-" }}
            </el-descriptions-item>
            <el-descriptions-item label="审核时间" :label-width="110">
              {{ parseTime(prefectInfo.updateTime) || "-" }}
            </el-descriptions-item>
          </el-descriptions>

          <div v-if="canAudit" class="mt12">
            <el-input v-model="auditOpinion" type="textarea" :rows="3" placeholder="请输入审核意见" />
            <div class="text-right mt12">
              <el-button
                type="primary"
                :loading="auditLoading"
                v-hasPermi="['project:prefect:second-review', 'project:prefect:third-review']"
                @click="handleApprove"
              >通过</el-button>
              <el-button
                type="danger"
                :loading="auditLoading"
                v-hasPermi="['project:prefect:second-review', 'project:prefect:third-review']"
                @click="handleReject"
              >拒绝</el-button>
            </div>
          </div>

          <el-divider content-position="left">历史审核意见</el-divider>
          <el-timeline v-if="opinionList.length">
            <el-timeline-item
              v-for="item in opinionList"
              :key="item.id || item.createTime || item.nodeCode"
              :timestamp="parseTime(item.createTime)"
              placement="top"
            >
              <div class="timeline-title">
                {{ item.nodeName || "-" }} · {{ item.operatorName || "-" }}
              </div>
              <div class="timeline-content">
                {{ item.opinionContent || "-" }}
              </div>
            </el-timeline-item>
          </el-timeline>
          <el-empty v-else description="暂无审核意见" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { parseTime } from "@/utils/ruoyi";
import { getProject, secondReviewProject, thirdReviewProject, updateProject } from "@/api/project/projects";

const { proxy } = getCurrentInstance();
const router = useRouter();
const route = useRoute();

const projectInfo = ref({});
const prefectInfo = ref({});
const opinionList = ref([]);

const activeTab = ref("contract");
const editMode = ref(false);
const saving = ref(false);

const auditOpinion = ref("");
const auditLoading = ref(false);

const stepItems = [
  { value: "01", title: "项目登记" },
  { value: "02", title: "工程师修改" },
  { value: "03", title: "二级复审" },
  { value: "04", title: "三级复审" },
  { value: "05", title: "待归档" },
  { value: "06", title: "已归档" }
];

const prefectStatusLabelMap = stepItems.reduce((acc, cur) => {
  acc[cur.value] = cur.title;
  return acc;
}, {});

const currentStatus = computed(() => {
  const status = prefectInfo.value?.currentStatus;
  if (status) return status;
  const fallback = projectInfo.value?.prefectStatus;
  if (fallback && typeof fallback === "string" && fallback.length === 2) return fallback;
  return undefined;
});

const currentStep = computed(() => {
  const idx = stepItems.findIndex(i => i.value === currentStatus.value);
  return idx >= 0 ? idx + 1 : 1;
});

const prefectStatusLabel = computed(() => {
  const s = currentStatus.value;
  if (!s) return "未知";
  return prefectStatusLabelMap[s] || s;
});

const prefectTagType = computed(() => {
  const s = currentStatus.value;
  if (s === "06") return "success";
  if (s === "05") return "warning";
  if (s === "03" || s === "04") return "danger";
  return "info";
});

const canAudit = computed(() => {
  return currentStatus.value === "03" || currentStatus.value === "04";
});

function goBack() {
  router.go(-1);
}

function toggleEdit() {
  editMode.value = !editMode.value;
  if (!editMode.value) {
    getProjectDetail();
  }
}

async function getProjectDetail() {
  const projectId = route.query.id || route.params.id;
  if (!projectId) return;
  const res = await getProject(projectId);
  const data = res?.data || {};
  projectInfo.value = data.projectInfo || data || {};
  prefectInfo.value = data.prefectInfo || {};
  opinionList.value = Array.isArray(data.opinionList) ? data.opinionList : [];
}

async function saveProject() {
  if (!projectInfo.value?.proId) {
    proxy.$modal.msgError("项目ID缺失，无法保存");
    return;
  }
  saving.value = true;
  try {
    await updateProject(projectInfo.value);
    proxy.$modal.msgSuccess("保存成功");
    editMode.value = false;
    await getProjectDetail();
  } finally {
    saving.value = false;
  }
}

async function handleApprove() {
  if (!canAudit.value) return;
  if (!auditOpinion.value || !auditOpinion.value.trim()) {
    proxy.$modal.msgError("请填写审核意见");
    return;
  }
  const proId = projectInfo.value?.proId;
  if (!proId) return;
  auditLoading.value = true;
  try {
    await proxy.$modal.confirm("确认通过该项目吗？");
    if (currentStatus.value === "03") {
      await secondReviewProject({ proId, currentStatus: "03", targetStatus: "04", opinionContent: auditOpinion.value });
    } else if (currentStatus.value === "04") {
      await thirdReviewProject({ proId, currentStatus: "04", targetStatus: "05", opinionContent: auditOpinion.value });
    }
    proxy.$modal.msgSuccess("操作成功");
    auditOpinion.value = "";
    await getProjectDetail();
  } catch (e) {
  } finally {
    auditLoading.value = false;
  }
}

async function handleReject() {
  if (!canAudit.value) return;
  if (!auditOpinion.value || !auditOpinion.value.trim()) {
    proxy.$modal.msgError("请填写审核意见");
    return;
  }
  const proId = projectInfo.value?.proId;
  if (!proId) return;
  auditLoading.value = true;
  try {
    await proxy.$modal.confirm("确认拒绝该项目吗？");
    if (currentStatus.value === "03") {
      await secondReviewProject({ proId, currentStatus: "03", targetStatus: "02", opinionContent: auditOpinion.value });
    } else if (currentStatus.value === "04") {
      await thirdReviewProject({ proId, currentStatus: "04", targetStatus: "02", opinionContent: auditOpinion.value });
    }
    proxy.$modal.msgSuccess("操作成功");
    auditOpinion.value = "";
    await getProjectDetail();
  } catch (e) {
  } finally {
    auditLoading.value = false;
  }
}

onMounted(() => {
  getProjectDetail();
});
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.page-title .title {
  font-weight: 600;
  font-size: 16px;
  line-height: 22px;
}
.page-title .sub {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 6px;
  flex-wrap: wrap;
}
.sub-item {
  color: #909399;
  font-size: 12px;
}
.page-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.card-title {
  font-weight: 600;
}
.mt12 {
  margin-top: 12px;
}
.timeline-title {
  font-weight: 600;
  line-height: 20px;
}
.timeline-content {
  margin-top: 4px;
  color: #606266;
  line-height: 20px;
}
</style>
