<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="80px">
      <el-form-item label="合同名称" prop="contractName">
        <el-input
          v-model="queryParams.contractName"
          placeholder="请输入合同名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="合同类型" prop="contractType">
        <el-select v-model="queryParams.contractType" placeholder="请选择合同类型" clearable style="width: 240px">
          <el-option v-for="item in contractTypeOptions" :key="item.value" :label="item.label" :value="item.value" />
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
          type="primary"
          plain
          icon="Plus"
          @click="handleAdd"
          v-hasPermi="['project:contract:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['project:contract:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['project:contract:remove']"
        >删除</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="contractList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" width="55" type="index" align="center" fixed="left">
        <template #default="scope">
          <span>{{ (queryParams.pageNum - 1) * queryParams.pageSize + scope.$index + 1 }}</span>
        </template>
      </el-table-column>
      <el-table-column label="合同名称" align="center" prop="contractName" min-width="180" show-overflow-tooltip />
      <el-table-column label="合同类型" align="center" prop="contractType" min-width="120" show-overflow-tooltip />
      <el-table-column label="合同金额" align="center" prop="contractAmount" min-width="120" />
      <el-table-column label="合同状态" align="center" prop="contractStatus" min-width="120" show-overflow-tooltip />
      <el-table-column label="签署日期" align="center" prop="contractSignDate" min-width="110" />
      <el-table-column label="生效日期" align="center" prop="contractEffectiveDate" min-width="110" />
      <el-table-column label="过期日期" align="center" prop="contractExpireDate" min-width="110" />
      <el-table-column label="终止日期" align="center" prop="contractTerminateDate" min-width="110" />
      <el-table-column label="操作人" align="center" prop="contractOperator" min-width="110" show-overflow-tooltip />
      <el-table-column label="创建时间" align="center" prop="createTime" min-width="160" show-overflow-tooltip />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width" fixed="right" width="220">
        <template #default="scope">
          <el-button
            link
            type="primary"
            icon="View"
            @click="handleView(scope.row)"
            v-hasPermi="['project:contract:query']"
          >详情</el-button>
          <el-button
            link
            type="primary"
            icon="Edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['project:contract:edit']"
          >修改</el-button>
          <el-button
            link
            type="danger"
            icon="Delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['project:contract:remove']"
          >删除</el-button>
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

    <el-dialog :title="title" v-model="open" width="860px" append-to-body>
      <el-form ref="contractRef" :model="form" :rules="rules" label-width="100px">
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="合同名称" prop="contractName">
              <el-input v-model="form.contractName" placeholder="请输入合同名称" :disabled="formMode === 'view'" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="合同类型" prop="contractType">
              <el-select
                v-model="form.contractType"
                placeholder="请选择合同类型"
                clearable
                style="width: 100%"
                :disabled="formMode === 'view'"
              >
                <el-option v-for="item in contractTypeOptions" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="合同金额" prop="contractAmount">
              <el-input-number
                v-model="form.contractAmount"
                :precision="2"
                :step="0.01"
                :min="0"
                controls-position="right"
                style="width: 100%"
                :disabled="formMode === 'view'"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="合同状态" prop="contractStatus">
              <el-select
                v-model="form.contractStatus"
                placeholder="请选择合同状态"
                clearable
                style="width: 100%"
                :disabled="formMode === 'view'"
              >
                <el-option v-for="item in contractStatusOptions" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="签署日期" prop="contractSignDate">
              <el-date-picker
                v-model="form.contractSignDate"
                type="date"
                value-format="YYYY-MM-DD"
                placeholder="请选择签署日期"
                style="width: 100%"
                :disabled="formMode === 'view'"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="生效日期" prop="contractEffectiveDate">
              <el-date-picker
                v-model="form.contractEffectiveDate"
                type="date"
                value-format="YYYY-MM-DD"
                placeholder="请选择生效日期"
                style="width: 100%"
                :disabled="formMode === 'view'"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="过期日期" prop="contractExpireDate">
              <el-date-picker
                v-model="form.contractExpireDate"
                type="date"
                value-format="YYYY-MM-DD"
                placeholder="请选择过期日期"
                style="width: 100%"
                :disabled="formMode === 'view'"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="终止日期" prop="contractTerminateDate">
              <el-date-picker
                v-model="form.contractTerminateDate"
                type="date"
                value-format="YYYY-MM-DD"
                placeholder="请选择终止日期"
                style="width: 100%"
                :disabled="formMode === 'view'"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="合同操作人" prop="contractOperator">
              <el-input v-model="form.contractOperator" placeholder="请输入合同操作人" :disabled="formMode === 'view'" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button v-if="formMode !== 'view'" type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="open = false">关 闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="ProjectContract">
import { addContract, delContract, getContract, listContract, updateContract } from "@/api/project/contract";

const { proxy } = getCurrentInstance();

const contractList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const formMode = ref("add");

const contractTypeOptions = [
  { value: "项目合同", label: "项目合同" },
  { value: "服务合同", label: "服务合同" },
  { value: "其他", label: "其他" }
];

const contractStatusOptions = [
  { value: "已签署", label: "已签署" },
  { value: "已过期", label: "已过期" },
  { value: "已终止", label: "已终止" }
];

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    contractName: undefined,
    contractType: undefined
  },
  rules: {
    contractName: [{ required: true, message: "合同名称不能为空", trigger: "blur" }],
    contractType: [{ required: true, message: "合同类型不能为空", trigger: "change" }]
  }
});

const { queryParams, form, rules } = toRefs(data);

function getList() {
  loading.value = true;
  listContract(queryParams.value).then((res) => {
    const payload = res?.data && (typeof res.data === "object") && ("code" in res.data || "msg" in res.data) ? res.data : res;
    const pageData = payload?.data || payload;
    contractList.value = pageData?.rows || [];
    total.value = pageData?.total || 0;
    loading.value = false;
  });
}

function reset() {
  form.value = {
    contractId: undefined,
    contractName: undefined,
    contractType: undefined,
    contractAmount: undefined,
    contractStatus: undefined,
    contractSignDate: undefined,
    contractEffectiveDate: undefined,
    contractExpireDate: undefined,
    contractTerminateDate: undefined,
    contractOperator: undefined
  };
  proxy.resetForm("contractRef");
}

function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

function resetQuery() {
  proxy.resetForm("queryRef");
  handleQuery();
}

function handleSelectionChange(selection) {
  ids.value = selection.map((item) => item.contractId);
  single.value = selection.length !== 1;
  multiple.value = !selection.length;
}

function handleAdd() {
  reset();
  formMode.value = "add";
  open.value = true;
  title.value = "新增合同";
}

function handleUpdate(row) {
  reset();
  formMode.value = "edit";
  const contractId = row?.contractId || ids.value?.[0];
  getContract(contractId).then((res) => {
    const payload = res?.data && (typeof res.data === "object") && ("code" in res.data || "msg" in res.data) ? res.data : res;
    form.value = payload?.data || payload || {};
    open.value = true;
    title.value = "修改合同";
  });
}

function handleView(row) {
  reset();
  formMode.value = "view";
  getContract(row.contractId).then((res) => {
    const payload = res?.data && (typeof res.data === "object") && ("code" in res.data || "msg" in res.data) ? res.data : res;
    form.value = payload?.data || payload || {};
    open.value = true;
    title.value = "合同详情";
  });
}

function submitForm() {
  proxy.$refs["contractRef"].validate((valid) => {
    if (valid) {
      if (form.value.contractId != null) {
        updateContract(form.value).then(() => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addContract(form.value).then(() => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}

function handleDelete(row) {
  const contractIds = row?.contractId || ids.value.join(",");
  proxy.$modal
    .confirm('是否确认删除合同编号为"' + contractIds + '"的数据项？')
    .then(function () {
      return delContract(contractIds);
    })
    .then(() => {
      getList();
      proxy.$modal.msgSuccess("删除成功");
    })
    .catch(() => {});
}

getList();
</script>
