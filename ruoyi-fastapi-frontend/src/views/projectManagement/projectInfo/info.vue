<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="130px">
<!--      <el-form-item label="项目编码" prop="projectCode">-->
<!--        <el-input-->
<!--          v-model="queryParams.projectCode"-->
<!--          placeholder="请输入项目编码"-->
<!--          clearable-->
<!--          style="width: 240px"-->
<!--          @keyup.enter="handleQuery"-->
<!--        />-->
<!--      </el-form-item>-->
      <el-form-item label="项目全称" prop="projectName">
        <el-input
          v-model="queryParams.projectName"
          placeholder="请输入项目全称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="项目类型" prop="projectType">
        <el-select v-model="queryParams.projectType" placeholder="请选择项目类型" clearable style="width: 240px">

        </el-select>
      </el-form-item>
      <el-form-item label="负责人" prop="projectManager">
        <el-select v-model="queryParams.projectManager" placeholder="请选择负责人" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
        <!-- 切换按钮 -->
        <el-button :icon="showAllSearch ? 'ArrowUp' : 'ArrowDown'" @click="toggleSearchItems">
          {{ showAllSearch ? '收起' : '展开' }}
        </el-button>
    </el-form-item>
      <template v-if="showAllSearch">
<!--      <el-form-item label="项目所属企业ID" prop="entId">-->
<!--        <el-input-->
<!--          v-model="queryParams.entId"-->
<!--          placeholder="请输入项目所属企业ID"-->
<!--          clearable-->
<!--          style="width: 240px"-->
<!--          @keyup.enter="handleQuery"-->
<!--        />-->
<!--      </el-form-item>-->
      <el-form-item label="业主单位" prop="entName">
        <el-select v-model="queryParams.entName" placeholder="请选择业主单位" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item label="使用单位" prop="userCompany">
        <el-select v-model="queryParams.userCompany" placeholder="请选择使用单位" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>

      <el-form-item label="项目成员" prop="coordinator">
        <el-select v-model="queryParams.coordinator" placeholder="请选择项目成员" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
<!--      <el-form-item label="合同签订状态" prop="contractSigned">-->
<!--        <el-select v-model="queryParams.contractSigned" placeholder="请选择合同签订状态" clearable style="width: 240px">-->
<!--          <el-option label="请选择字典生成" value="" />-->
<!--        </el-select>-->
<!--      </el-form-item>-->
<!--      <el-form-item label="是否已取" prop="documentObtained">-->
<!--        <el-select v-model="queryParams.documentObtained" placeholder="请选择是否已取" clearable style="width: 240px">-->
<!--          <el-option label="请选择字典生成" value="" />-->
<!--        </el-select>-->
<!--      </el-form-item>-->

      <el-form-item label="项目成果完成状态" prop="deliverableCompleted">
        <el-select v-model="queryParams.deliverableCompleted" placeholder="请选择项目成果完成状态" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>

      <el-form-item label="是否已请款" prop="paymentApplied">
        <el-select v-model="queryParams.paymentApplied" placeholder="请选择是否已请款" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item label="请款月份" prop="paymentMonth">
        <el-date-picker
          v-model="queryParams.paymentMonth"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择请款月份"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="是否已开票" prop="invoiceIssued">
        <el-select v-model="queryParams.invoiceIssued" placeholder="请选择是否已开票" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item label="开具日期" prop="invoiceDate">
        <el-date-picker
          v-model="queryParams.invoiceDate"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择开具日期"
          clearable
          style="width: 240px"
        />
      </el-form-item>


      <el-form-item label="业主是否已回款" prop="paymentReceived">
        <el-select v-model="queryParams.paymentReceived" placeholder="请选择业主是否已回款" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>

      <el-form-item label="回款日期" prop="paymentReceivedDate">
        <el-date-picker
          v-model="queryParams.paymentReceivedDate"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择回款日期"
          clearable
          style="width: 240px"
        />
      </el-form-item>


      <el-form-item label="是否已对账" prop="reconciliationDone">
        <el-select v-model="queryParams.reconciliationDone" placeholder="请选择是否已对账" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item label="对账日期" prop="reconciliationDate">
        <el-date-picker
          v-model="queryParams.reconciliationDate"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择对账日期"
          clearable
          style="width: 240px"
        />
      </el-form-item>

      <el-form-item label="是否已计提提成" prop="commissionAccrued">
        <el-select v-model="queryParams.commissionAccrued" placeholder="请选择是否已计提提成" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>

      <el-form-item label="提成计提日期" prop="commissionDate">
        <el-date-picker
          v-model="queryParams.commissionDate"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择提成计提日期"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="合同电子档是否已存档" prop="contractElectronicSaved">
        <el-input
          v-model="queryParams.contractElectronicSaved"
          placeholder="请输入合同电子档是否已存档"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="成果文件电子档是否已存档" prop="deliverableElectronicSaved">
        <el-input
          v-model="queryParams.deliverableElectronicSaved"
          placeholder="请输入成果文件电子档是否已存档"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>



      <el-form-item label="项目开始时间" prop="startDate">
        <el-date-picker
          v-model="queryParams.startDate"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择项目开始时间"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="项目预计结束时间" prop="endDate">
        <el-date-picker
          v-model="queryParams.endDate"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择项目预计结束时间"
          clearable
          style="width: 240px"
        />
      </el-form-item>

      <el-form-item label="项目状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择项目状态" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item label="流程状态" prop="prefectStatus">
        <el-select v-model="queryParams.prefectStatus" placeholder="请选择项目流程状态" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>

        </template>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="Plus"
          @click="handleViewAdd"
          v-hasPermi="['system:project:add']"
        >新增</el-button>
      </el-col>
<!--      <el-col :span="1.5">-->
<!--        <el-button-->
<!--          type="success"-->
<!--          plain-->
<!--          icon="Edit"-->
<!--          :disabled="single"-->
<!--          @click="handleUpdate"-->
<!--          v-hasPermi="['system:project1:edit']"-->
<!--        >修改</el-button>-->
<!--      </el-col>-->
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['system:project:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['system:project:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="projectList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
<!--      <el-table-column label="项目ID" align="center" prop="proId" />-->
      <el-table-column label="序号" width="55" type="index" align="center" fixed="left">
            <template #default="scope">
               <span>{{ (pageNum - 1) * pageSize + scope.$index + 1 }}</span>
            </template>
         </el-table-column>
      <el-table-column label="项目编码" align="center" prop="projectCode"  fixed="left"/>
      <el-table-column label="项目全称" align="center" prop="projectName" width="280" fixed="left"/>
      <el-table-column label="项目类型" align="center" prop="projectType"  fixed="left"/>
<!--      <el-table-column label="项目所属企业ID" align="center" prop="entId" />-->
      <el-table-column label="业主单位" align="center" prop="entName" />
      <el-table-column label="服务内容" align="center" prop="serviceContent" />
      <el-table-column label="使用单位" align="center" prop="userCompany" />
      <el-table-column label="负责人" align="center" prop="projectManager" />
      <el-table-column label="项目成员" align="center" prop="coordinator" />
      <el-table-column label="合同签订状态" align="center" prop="contractSigned" />
      <el-table-column label="是否已取" align="center" prop="documentObtained" />
      <el-table-column label="合同金额" align="center" prop="contractAmount" />
      <el-table-column label="合同折扣情况" align="center" prop="contractDiscount" />
      <el-table-column label="项目成果完成状态" align="center" prop="deliverableCompleted" />
      <el-table-column label="项目金额" align="center" prop="controlPriceReview" />
<!--      <el-table-column label="结算送审金额" align="center" prop="settlementSubmitted" />-->
<!--      <el-table-column label="结算审定金额" align="center" prop="settlementApproved" />-->
      <el-table-column label="项目应开票金额" align="center" prop="invoiceShouldAmount" />
      <el-table-column label="是否已请款" align="center" prop="paymentApplied" />
      <el-table-column label="请款月份" align="center" prop="paymentMonth" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.paymentMonth, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="是否已开票" align="center" prop="invoiceIssued" />
      <el-table-column label="开具日期" align="center" prop="invoiceDate" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.invoiceDate, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="已开票金额" align="center" prop="invoiceIssuedAmount" />
      <el-table-column label="剩余已开票金额" align="center" prop="invoiceRemainingAmount" />
      <el-table-column label="业主是否已回款" align="center" prop="paymentReceived" />
      <el-table-column label="已回款金额" align="center" prop="paymentReceivedAmount" />
      <el-table-column label="回款日期" align="center" prop="paymentReceivedDate" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.paymentReceivedDate, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="剩余未回款金额" align="center" prop="paymentRemainingAmount" />
      <el-table-column label="项目回款率" align="center" prop="paymentRecoveryRate" />
      <el-table-column label="是否已对账" align="center" prop="reconciliationDone" />
      <el-table-column label="对账日期" align="center" prop="reconciliationDate" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.reconciliationDate, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="对账凭证" align="center" prop="reconciliationVoucher" />
      <el-table-column label="是否已计提提成" align="center" prop="commissionAccrued" />
      <el-table-column label="提成金额" align="center" prop="commissionAmount" />
      <el-table-column label="提成计提日期" align="center" prop="commissionDate" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.commissionDate, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="合同电子档是否已存档" align="center" prop="contractElectronicSaved" />
      <el-table-column label="合同文件编号" align="center" prop="contractFile" />
      <el-table-column label="成果文件电子档是否已存档" align="center" prop="deliverableElectronicSaved" />
      <el-table-column label="成果文件编号" align="center" prop="deliverableFile" />
      <el-table-column label="纸质资料存档情况" align="center" prop="documentPaperSaved" />
      <el-table-column label="资料存档类型说明" align="center" prop="documentSaveType" />
      <el-table-column label="项目其他备注信息" align="center" prop="remarks" />
      <el-table-column label="项目开始时间" align="center" prop="startDate" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.startDate, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="项目预计结束时间" align="center" prop="endDate" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.endDate, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="项目预算" align="center" prop="projectBudget" />
      <el-table-column label="项目描述" align="center" prop="projectDesc" />
      <el-table-column label="项目状态" align="center" prop="status" />
      <el-table-column label="项目流程状态" align="center" prop="prefectStatus" />
      <el-table-column label="创建人名称" align="center" prop="createName" />
      <el-table-column label="更新人名称" align="center" prop="updateName" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width" width="200" fixed="right">
        <template #default="scope">
          <el-button link type="primary" icon="View" @click="handleView(scope.row)">查看</el-button>
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['system:project:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['system:project:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改项目主对话框 -->
    <el-dialog :title="title" v-model="open" width="60%" append-to-body>
      <el-form ref="project1Ref" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="项目编码" prop="projectCode">
        <el-input v-model="form.projectCode" placeholder="请输入项目编码" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目全称" prop="projectName">
        <el-input v-model="form.projectName" placeholder="请输入项目全称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目类型" prop="projectType">
        <el-select v-model="form.projectType" placeholder="请选择项目类型">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="业主单位" prop="entName">
        <el-select v-model="form.entName" placeholder="请选择业主单位">
          <el-option
            v-for="item in entList"
            :key="item.entId"
            :label="item.enterpriseName"
            :value="item.entId"
          />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="服务内容" prop="serviceContent">
        <el-select v-model="form.serviceContent" placeholder="请选择服务内容">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="使用单位" prop="userCompany">
        <el-select v-model="form.userCompany" placeholder="请选择使用单位">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="负责人" prop="projectManager">
        <el-select v-model="form.projectManager" placeholder="请选择负责人">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目成员" prop="coordinator">
        <el-select v-model="form.coordinator" placeholder="请选择项目成员">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="合同签订状态" prop="contractSigned">
        <el-select v-model="form.contractSigned" placeholder="请选择合同签订状态">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="是否已取" prop="documentObtained">
        <el-select v-model="form.documentObtained" placeholder="请选择是否已取">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="合同金额" prop="contractAmount">
        <el-input v-model="form.contractAmount" placeholder="请输入合同金额" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="合同折扣情况" prop="contractDiscount">
        <el-input v-model="form.contractDiscount" placeholder="请输入合同折扣情况" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目成果完成状态" prop="deliverableCompleted">
        <el-select v-model="form.deliverableCompleted" placeholder="请选择项目成果完成状态">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="控制价或控制价评审" prop="controlPriceReview">
        <el-input v-model="form.controlPriceReview" placeholder="请输入控制价或控制价评审" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="结算送审金额" prop="settlementSubmitted">
        <el-input v-model="form.settlementSubmitted" placeholder="请输入结算送审金额" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="结算审定金额" prop="settlementApproved">
        <el-input v-model="form.settlementApproved" placeholder="请输入结算审定金额" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目应开票金额" prop="invoiceShouldAmount">
        <el-input v-model="form.invoiceShouldAmount" placeholder="请输入项目应开票金额" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="是否已请款" prop="paymentApplied">
        <el-select v-model="form.paymentApplied" placeholder="请选择是否已请款">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="请款月份" prop="paymentMonth">
        <el-date-picker clearable
          v-model="form.paymentMonth"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择请款月份">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="是否已开票" prop="invoiceIssued">
        <el-select v-model="form.invoiceIssued" placeholder="请选择是否已开票">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="开具日期" prop="invoiceDate">
        <el-date-picker clearable
          v-model="form.invoiceDate"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择开具日期">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="已开票金额" prop="invoiceIssuedAmount">
        <el-input v-model="form.invoiceIssuedAmount" placeholder="请输入已开票金额" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="剩余已开票金额" prop="invoiceRemainingAmount">
        <el-input v-model="form.invoiceRemainingAmount" placeholder="请输入剩余已开票金额" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="业主是否已回款" prop="paymentReceived">
        <el-select v-model="form.paymentReceived" placeholder="请选择业主是否已回款">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="已回款金额" prop="paymentReceivedAmount">
        <el-input v-model="form.paymentReceivedAmount" placeholder="请输入已回款金额" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="回款日期" prop="paymentReceivedDate">
        <el-date-picker clearable
          v-model="form.paymentReceivedDate"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择回款日期">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="剩余未回款金额" prop="paymentRemainingAmount">
        <el-input v-model="form.paymentRemainingAmount" placeholder="请输入剩余未回款金额" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目回款率" prop="paymentRecoveryRate">
        <el-input v-model="form.paymentRecoveryRate" placeholder="请输入项目回款率" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="是否已对账" prop="reconciliationDone">
        <el-select v-model="form.reconciliationDone" placeholder="请选择是否已对账">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="对账日期" prop="reconciliationDate">
        <el-date-picker clearable
          v-model="form.reconciliationDate"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择对账日期">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="对账凭证" prop="reconciliationVoucher">
        <el-input v-model="form.reconciliationVoucher" placeholder="请输入对账凭证" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="是否已计提成" prop="commissionAccrued">
        <el-select v-model="form.commissionAccrued" placeholder="请选择是否已计提成">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="提成金额" prop="commissionAmount">
        <el-input v-model="form.commissionAmount" placeholder="请输入提成金额" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="提成计提日期" prop="commissionDate">
        <el-date-picker clearable
          v-model="form.commissionDate"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择提成计提日期">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="合同电子档是否已存档" prop="contractElectronicSaved">
        <el-input v-model="form.contractElectronicSaved" placeholder="请输入合同电子档是否已存档" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="合同文件编号" prop="contractFile">
        <file-upload v-model="form.contractFile"/>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="成果文件电子档是否已存档" prop="deliverableElectronicSaved">
        <el-input v-model="form.deliverableElectronicSaved" placeholder="请输入成果文件电子档是否已存档" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="成果文件编号" prop="deliverableFile">
        <file-upload v-model="form.deliverableFile"/>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="纸质资料存档情况" prop="documentPaperSaved">
        <el-select v-model="form.documentPaperSaved" placeholder="请选择纸质资料存档情况">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="资料存档类型说明" prop="documentSaveType">
        <el-select v-model="form.documentSaveType" placeholder="请选择资料存档类型说明">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目其他备注信息" prop="remarks">
        <el-input v-model="form.remarks" placeholder="请输入项目其他备注信息" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目开始时间" prop="startDate">
        <el-date-picker clearable
          v-model="form.startDate"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择项目开始时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目预计结束时间" prop="endDate">
        <el-date-picker clearable
          v-model="form.endDate"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择项目预计结束时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目预算" prop="projectBudget">
        <el-input v-model="form.projectBudget" placeholder="请输入项目预算" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目描述" prop="projectDesc">
        <el-input v-model="form.projectDesc" type="textarea" placeholder="请输入内容" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目状态" prop="status">
        <el-radio-group v-model="form.status">
          <el-radio label="请选择字典生成" value="" />
        </el-radio-group>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="项目流程状态" prop="prefectStatus">
        <el-radio-group v-model="form.prefectStatus">
          <el-radio label="请选择字典生成" value="" />
        </el-radio-group>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="创建人名称" prop="createName">
        <el-input v-model="form.createName" placeholder="请输入创建人名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="更新人名称" prop="updateName">
        <el-input v-model="form.updateName" placeholder="请输入更新人名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, false)" label="删除标志" prop="delFlag">
        <el-input v-model="form.delFlag" placeholder="请输入删除标志" />
      </el-form-item>

      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="Project1">
import { listProject, getProject, delProject, addProject, updateProject } from "@/api/project/projects";
import {listEnt} from "@/api/project/enterprise.js";

const { proxy } = getCurrentInstance();

const projectList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const pageNum = ref(1);
const pageSize = ref(10);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const entList = ref([]);
const userCompanyList = ref([])

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    projectCode: null,
    projectName: null,
    projectType: null,
    entId: null,
    entName: null,
    serviceContent: null,
    userCompany: null,
    projectManager: null,
    coordinator: null,
    contractSigned: null,
    documentObtained: null,
    contractAmount: null,
    contractDiscount: null,
    deliverableCompleted: null,
    controlPriceReview: null,
    settlementSubmitted: null,
    settlementApproved: null,
    invoiceShouldAmount: null,
    paymentApplied: null,
    paymentMonth: null,
    invoiceIssued: null,
    invoiceDate: null,
    invoiceIssuedAmount: null,
    invoiceRemainingAmount: null,
    paymentReceived: null,
    paymentReceivedAmount: null,
    paymentReceivedDate: null,
    paymentRemainingAmount: null,
    paymentRecoveryRate: null,
    reconciliationDone: null,
    reconciliationDate: null,
    reconciliationVoucher: null,
    commissionAccrued: null,
    commissionAmount: null,
    commissionDate: null,
    contractElectronicSaved: null,
    contractFile: null,
    deliverableElectronicSaved: null,
    deliverableFile: null,
    documentPaperSaved: null,
    documentSaveType: null,
    remarks: null,
    startDate: null,
    endDate: null,
    projectBudget: null,
    projectDesc: null,
    status: null,
    prefectStatus: null,
    createName: null,
    updateName: null,
  },
  rules: {
  }
});

const { queryParams, form, rules } = toRefs(data);
const showAllSearch = ref(false); // 控制搜索框展开状态
import { useRouter } from 'vue-router'

const router = useRouter()

// 切换搜索项显示状态
function toggleSearchItems() {
  showAllSearch.value = !showAllSearch.value;
}

// 从 API 获取选项数据
// onMounted(() => {
//   getProjectTypeOptions(); // 获取项目类型字典
// });
// const { proxy } = getCurrentInstance();
const { sys_normal_disable, sys_user_sex } = proxy.useDict(
  "sys_normal_disable",
  "sys_user_sex"
);

function getProjectTypeOptions() {
  // 调用 API 获取字典数据
  listEnt({entType:1}).then(response => {
    entList.value = response.data.rows;
    // console.log("entlist",entList.value)
  });
}


/** 查询项目主列表 */
function getList() {
  loading.value = true;
  listProject(queryParams.value).then(response => {
    projectList.value = response.data.rows;
    total.value = response.data.total;
    loading.value = false;
  });
}

/** 取消按钮 */
function cancel() {
  open.value = false;
  reset();
}

/** 表单重置 */
function reset() {
  form.value = {
    proId: null,
    projectCode: null,
    projectName: null,
    projectType: null,
    entId: null,
    entName: null,
    serviceContent: null,
    userCompany: null,
    projectManager: null,
    coordinator: null,
    contractSigned: null,
    documentObtained: null,
    contractAmount: null,
    contractDiscount: null,
    deliverableCompleted: null,
    controlPriceReview: null,
    settlementSubmitted: null,
    settlementApproved: null,
    invoiceShouldAmount: null,
    paymentApplied: null,
    paymentMonth: null,
    invoiceIssued: null,
    invoiceDate: null,
    invoiceIssuedAmount: null,
    invoiceRemainingAmount: null,
    paymentReceived: null,
    paymentReceivedAmount: null,
    paymentReceivedDate: null,
    paymentRemainingAmount: null,
    paymentRecoveryRate: null,
    reconciliationDone: null,
    reconciliationDate: null,
    reconciliationVoucher: null,
    commissionAccrued: null,
    commissionAmount: null,
    commissionDate: null,
    contractElectronicSaved: null,
    contractFile: null,
    deliverableElectronicSaved: null,
    deliverableFile: null,
    documentPaperSaved: null,
    documentSaveType: null,
    remarks: null,
    startDate: null,
    endDate: null,
    projectBudget: null,
    projectDesc: null,
    status: null,
    prefectStatus: null,
    createBy: null,
    createName: null,
    createTime: null,
    updateBy: null,
    updateName: null,
    updateTime: null,
    delFlag: null,
  };
  proxy.resetForm("project1Ref");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  proxy.resetForm("queryRef");
  handleQuery();
}

/** 多选框选中数据  */
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.proId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  // getProjectTypeOptions()
  open.value = true;
  title.value = "添加项目主";
}

// 查看详情
function handleView(row) {
  router.push({
    path: '/projectManagement/detail',
    query: {
      id: row.proId,
      type: 'view'
    }
  })
}

// 新增
function handleViewAdd(row) {
  router.push({
    path: '/projectManagement/detail',
    query: {
      type: 'add',
      title: "添加项目主",
    }
  })
}


/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  getProjectTypeOptions();
  // const _proId = row.proId || ids.value;
  // getProject(_proId).then(response => {
  //   form.value = response.data.projectInfo;
  //   open.value = true;
  //   title.value = "修改项目主";
  // });
  router.push({
    path: '/projectManagement/detail',
    query: {
      type: 'edit', // 标识是编辑操作
      id: row.proId // 传递项目ID，用于详情页获取数据
    }
  })
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["project1Ref"].validate(valid => {
    if (valid) {
      if (form.value.proId != null) {
        updateProject(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addProject(form.value).then(response => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const _proIds = row.proId || ids.value;
  proxy.$modal.confirm('是否确认删除项目主编号为"' + _proIds + '"的数据项？').then(function() {
    return delProject(_proIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('system/project1/export', {
    ...queryParams.value
  }, `project1_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.proId == null ? insert : edit;
}

getList();

</script>