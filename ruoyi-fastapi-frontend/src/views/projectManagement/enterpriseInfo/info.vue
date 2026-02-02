<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="120px">
      <el-form-item label="单位名称" prop="enterpriseName">
        <el-input
          v-model="queryParams.enterpriseName"
          placeholder="请输入单位名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="纳税人识别号" prop="taxpayerId">
        <el-input
          v-model="queryParams.taxpayerId"
          placeholder="请输入纳税人识别号"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="单位类型" prop="entType">
        <el-select v-model="queryParams.entType" placeholder="请选择单位类型">
          <el-option v-for="item in ent_type" :key="item.value" :label="item.label" :value="item.value"/>
        </el-select>
      </el-form-item>
      <el-form-item label="单位地址" prop="address">
        <el-input
          v-model="queryParams.address"
          placeholder="请输入单位地址"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="联系人" prop="contactPerson">
        <el-input
          v-model="queryParams.contactPerson"
          placeholder="请输入联系人"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="联系电话" prop="contactPhone">
        <el-input
          v-model="queryParams.contactPhone"
          placeholder="请输入联系电话"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="开户行" prop="bankName">
        <el-input
          v-model="queryParams.bankName"
          placeholder="请输入开户行"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="银行账号" prop="bankAccount">
        <el-input
          v-model="queryParams.bankAccount"
          placeholder="请输入银行账号"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
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
          v-hasPermi="['system:info:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['system:info:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['system:info:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['system:info:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="infoList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
<!--      <el-table-column label="主键ID" align="center" prop="id" />-->
      <el-table-column label="序号" width="55" type="index" align="center" fixed="left">
            <template #default="scope">
               <span>{{ (pageNum - 1) * pageSize + scope.$index + 1 }}</span>
            </template>
         </el-table-column>
      <el-table-column label="单位名称" align="center" prop="enterpriseName" />
      <el-table-column label="纳税人识别号" align="center" prop="taxpayerId" />
      <el-table-column label="单位类型" align="center" prop="entType" >
<!--        <template #default="scope">-->
<!--          <el-tag v-for="item in ent_type" :key="item.value" v-if="scope.row.entType == item.value">{{ item.label }}</el-tag>-->
<!--        </template>-->
<!--        {{entTypeDoneLabel}}-->
      </el-table-column>
      <el-table-column label="单位地址" align="center" prop="address" />
      <el-table-column label="联系人" align="center" prop="contactPerson" />
      <el-table-column label="联系电话" align="center" prop="contactPhone" />
      <el-table-column label="开户行" align="center" prop="bankName" />
      <el-table-column label="银行账号" align="center" prop="bankAccount" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['system:info:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['system:info:remove']">删除</el-button>
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

    <!-- 添加或修改单位基本信息对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="infoRef" :model="form" :rules="rules" label-width="110px">
      <el-form-item v-if="renderField(true, true)" label="单位名称" prop="enterpriseName">
        <el-input v-model="form.enterpriseName" placeholder="请输入单位名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="纳税人识别号" prop="taxpayerId">
        <el-input v-model="form.taxpayerId" placeholder="请输入纳税人识别号" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="单位类型" prop="taxpayerId">
        <el-select v-model="form.entType" placeholder="请选择单位类型">
          <el-option v-for="item in ent_type" :key="item.value" :label="item.label" :value="item.value"/>
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="单位地址" prop="address">
        <el-input v-model="form.address" placeholder="请输入单位地址" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="联系人" prop="contactPerson">
        <el-input v-model="form.contactPerson" placeholder="请输入联系人" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="联系电话" prop="contactPhone">
        <el-input v-model="form.contactPhone" placeholder="请输入联系电话" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="开户行" prop="bankName">
        <el-input v-model="form.bankName" placeholder="请输入开户行" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="银行账号" prop="bankAccount">
        <el-input v-model="form.bankAccount" placeholder="请输入银行账号" />
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

<script setup name="Info">
import { listEnt, getEnt, addEnt, updateEnt, delEnt } from "@/api/project/enterprise";
import {computed} from "vue";

const { proxy } = getCurrentInstance();

const infoList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const pageNum = ref(1);
const pageSize = ref(10);

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    enterpriseName: null,
    entType: null,
    taxpayerId: null,
    address: null,
    contactPerson: null,
    contactPhone: null,
    bankName: null,
    bankAccount: null,
  },
  rules: {
    enterpriseName: [
      { required: true, message: "单位名称不能为空", trigger: "blur" }
    ],
    taxpayerId: [
      { required: true, message: "纳税人识别号不能为空", trigger: "blur" }
    ],
    entType: [
      { required: true, message: "单位类型不能为空", trigger: "blur" }
    ],
    createTime: [
      { required: true, message: "创建时间不能为空", trigger: "blur" }
    ],
    updateTime: [
      { required: true, message: "更新时间不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

const { ent_type } = proxy.useDict(
  "ent_type"
);

const entTypeDoneLabel = computed(() => {
  console.log('form.value:', form.value)
  const value = form.value.entType;
  console.log('form.value2:', value)
  if (value === 0) return '业主单位';
  if (value === 1) return '使用单位';
  return '-';
});

/** 查询单位基本信息列表 */
function getList() {
  loading.value = true;
  listEnt(queryParams.value).then(response => {
    infoList.value = response.data.rows;
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
    id: null,
    enterpriseName: null,
    taxpayerId: null,
    entType: null,
    address: null,
    contactPerson: null,
    contactPhone: null,
    bankName: null,
    bankAccount: null,
    createTime: null,
    updateTime: null,
  };
  proxy.resetForm("infoRef");
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
  ids.value = selection.map(item => item.id);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加单位基本信息";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;

  getEnt(_id).then(response => {
    console.log(requestUrl)
    form.value = response.data;
    open.value = true;
    title.value = "修改单位基本信息";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["infoRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateEnt(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addEnt(form.value).then(response => {
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
  const _ids = row.id || ids.value;
  proxy.$modal.confirm('是否确认删除单位基本信息编号为"' + _ids + '"的数据项？').then(function() {
    return delEnt(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('system/info/export', {
    ...queryParams.value
  }, `info_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>