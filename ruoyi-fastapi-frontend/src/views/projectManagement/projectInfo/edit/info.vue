<template>
  <div class="app-container">
    <h2>项目详情</h2>

    <!-- 项目基本信息 -->
    <el-descriptions title="项目基本信息" :column="2" border>
      <el-descriptions-item label="项目编码">{{ projectDetail.projectCode }}</el-descriptions-item>
      <el-descriptions-item label="项目全称">{{ projectDetail.projectName }}</el-descriptions-item>
      <el-descriptions-item label="项目类型">{{ projectDetail.projectType }}</el-descriptions-item>
      <el-descriptions-item label="业主单位">{{ projectDetail.entName }}</el-descriptions-item>
      <el-descriptions-item label="服务内容">{{ projectDetail.serviceContent }}</el-descriptions-item>
      <el-descriptions-item label="使用单位">{{ projectDetail.userCompany }}</el-descriptions-item>
      <el-descriptions-item label="负责人">{{ projectDetail.projectManager }}</el-descriptions-item>
      <el-descriptions-item label="项目成员">{{ projectDetail.coordinator }}</el-descriptions-item>
      <el-descriptions-item label="合同金额">{{ projectDetail.contractAmount }}</el-descriptions-item>
      <el-descriptions-item label="项目金额">{{ projectDetail.controlPriceReview }}</el-descriptions-item>
      <el-descriptions-item label="项目开始时间">{{ parseTime(projectDetail.startDate, '{y}-{m}-{d}') }}</el-descriptions-item>
      <el-descriptions-item label="项目预计结束时间">{{ parseTime(projectDetail.endDate, '{y}-{m}-{d}') }}</el-descriptions-item>
      <el-descriptions-item label="项目状态">{{ projectDetail.status }}</el-descriptions-item>
      <el-descriptions-item label="项目流程状态">{{ projectDetail.prefectStatus }}</el-descriptions-item>
    </el-descriptions>

    <!-- 合同信息 -->
    <el-descriptions title="合同信息" :column="2" border style="margin-top: 20px;">
      <el-descriptions-item label="合同签订状态">{{ projectDetail.contractSigned }}</el-descriptions-item>
      <el-descriptions-item label="是否已取">{{ projectDetail.documentObtained }}</el-descriptions-item>
      <el-descriptions-item label="合同折扣情况">{{ projectDetail.contractDiscount }}</el-descriptions-item>
      <el-descriptions-item label="合同金额">{{ projectDetail.contractAmount }}</el-descriptions-item>
    </el-descriptions>

    <!-- 发票与回款信息 -->
    <el-descriptions title="发票与回款信息" :column="2" border style="margin-top: 20px;">
      <el-descriptions-item label="项目应开票金额">{{ projectDetail.invoiceShouldAmount }}</el-descriptions-item>
      <el-descriptions-item label="是否已请款">{{ projectDetail.paymentApplied }}</el-descriptions-item>
      <el-descriptions-item label="请款月份">{{ parseTime(projectDetail.paymentMonth, '{y}-{m}-{d}') }}</el-descriptions-item>
      <el-descriptions-item label="是否已开票">{{ projectDetail.invoiceIssued }}</el-descriptions-item>
      <el-descriptions-item label="开具日期">{{ parseTime(projectDetail.invoiceDate, '{y}-{m}-{d}') }}</el-descriptions-item>
      <el-descriptions-item label="已开票金额">{{ projectDetail.invoiceIssuedAmount }}</el-descriptions-item>
      <el-descriptions-item label="剩余已开票金额">{{ projectDetail.invoiceRemainingAmount }}</el-descriptions-item>
      <el-descriptions-item label="业主是否已回款">{{ projectDetail.paymentReceived }}</el-descriptions-item>
      <el-descriptions-item label="已回款金额">{{ projectDetail.paymentReceivedAmount }}</el-descriptions-item>
      <el-descriptions-item label="回款日期">{{ parseTime(projectDetail.paymentReceivedDate, '{y}-{m}-{d}') }}</el-descriptions-item>
      <el-descriptions-item label="剩余未回款金额">{{ projectDetail.paymentRemainingAmount }}</el-descriptions-item>
      <el-descriptions-item label="项目回款率">{{ projectDetail.paymentRecoveryRate }}</el-descriptions-item>
    </el-descriptions>

    <!-- 对账与提成信息 -->
    <el-descriptions title="对账与提成信息" :column="2" border style="margin-top: 20px;">
      <el-descriptions-item label="是否已对账">{{ projectDetail.reconciliationDone }}</el-descriptions-item>
      <el-descriptions-item label="对账日期">{{ parseTime(projectDetail.reconciliationDate, '{y}-{m}-{d}') }}</el-descriptions-item>
      <el-descriptions-item label="对账凭证">{{ projectDetail.reconciliationVoucher }}</el-descriptions-item>
      <el-descriptions-item label="是否已计提提成">{{ projectDetail.commissionAccrued }}</el-descriptions-item>
      <el-descriptions-item label="提成金额">{{ projectDetail.commissionAmount }}</el-descriptions-item>
      <el-descriptions-item label="提成计提日期">{{ parseTime(projectDetail.commissionDate, '{y}-{m}-{d}') }}</el-descriptions-item>
    </el-descriptions>

    <!-- 存档信息 -->
    <el-descriptions title="存档信息" :column="2" border style="margin-top: 20px;">
      <el-descriptions-item label="合同电子档是否已存档">{{ projectDetail.contractElectronicSaved }}</el-descriptions-item>
      <el-descriptions-item label="合同文件编号">{{ projectDetail.contractFile }}</el-descriptions-item>
      <el-descriptions-item label="成果文件电子档是否已存档">{{ projectDetail.deliverableElectronicSaved }}</el-descriptions-item>
      <el-descriptions-item label="成果文件编号">{{ projectDetail.deliverableFile }}</el-descriptions-item>
      <el-descriptions-item label="纸质资料存档情况">{{ projectDetail.documentPaperSaved }}</el-descriptions-item>
      <el-descriptions-item label="资料存档类型说明">{{ projectDetail.documentSaveType }}</el-descriptions-item>
    </el-descriptions>

    <!-- 操作按钮 -->
    <div class="button-group" style="margin-top: 20px; text-align: center;">
      <el-button @click="goBack">返回</el-button>
      <el-button type="primary" @click="handleEdit">编辑</el-button>
    </div>
  </div>
</template>

<script setup name="ProjectDetail">
import { getProject } from '@/api/project/projects';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const projectDetail = ref({});

// 获取项目详情
function getProjectDetail() {
  const projectId = route.query.id;
  if (projectId) {
    getProject(projectId).then(response => {
      projectDetail.value = response.data.projectInfo || response.data;
    });
  }
}

// 返回上一页
function goBack() {
  router.go(-1);
}

// 编辑项目
function handleEdit() {
  router.push({
    path: '/projectManagement/projectInfo/edit',
    query: { id: route.query.id }
  });
}

onMounted(() => {
  getProjectDetail();
});
</script>
