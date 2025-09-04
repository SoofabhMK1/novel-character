<template>
  <div class="lore-manager-container">
    <el-row :gutter="20">
      <!-- 左侧：类别导航 -->
      <el-col :xs="24" :sm="6">
        <el-card shadow="never">
          <template #header><strong>设定类别</strong></template>
          <el-menu
            :default-active="activeCategory"
            @select="handleCategorySelect"
          >
            <el-menu-item 
              v-for="category in loreCategories" 
              :key="category" 
              :index="category"
            >
              {{ category }}
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>

      <!-- 右侧：数据表格与操作 -->
      <el-col :xs="24" :sm="18">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>{{ activeCategory }} - 设定列表</span>
              <el-button type="primary" @click="handleOpenForm(null)">+ 新建设定</el-button>
            </div>
          </template>
          
          <el-table :data="loreEntries" v-loading="loading" border stripe>
            <el-table-column prop="key" label="键 (Key)" width="180" />
            <el-table-column prop="name" label="名称" width="180" />
            <el-table-column prop="description" label="描述" show-overflow-tooltip />
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="scope">
                <el-button link type="primary" size="small" @click="handleOpenForm(scope.row)">编辑</el-button>
                <el-button link type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 新建/编辑模态框 -->
    <el-dialog
      v-model="formDialogVisible"
      :title="isEditMode ? `编辑设定: ${formData.name}` : `新建设定 - ${activeCategory}`"
      width="600px"
      @close="resetForm"
    >
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="类别" prop="category">
          <el-input v-model="formData.category" disabled />
        </el-form-item>
        <el-form-item label="键 (Key)" prop="key">
          <el-select 
            v-model="formData.key" 
            placeholder="请选择一个枚举键" 
            style="width: 100%;"
            :disabled="isEditMode"
          >
            <el-option 
              v-for="item in availableKeysForCategory" 
              :key="item" 
              :label="item" 
              :value="item" 
            />
          </el-select>
          <div class="form-tip">
            "键"是与程序枚举对应的标准名称，创建后不可修改。
          </div>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="formData.name" placeholder="例如：人类" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" :rows="4" v-model="formData.description" />
        </el-form-item>
        <!-- 以后可以添加对 attributes (JSONB) 的编辑器 -->
      </el-form>
      <template #footer>
        <el-button @click="formDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import api from '../services/api';

// --- 状态定义 ---
const allEnums = reactive({}); 
const loading = ref(false);
const loreCategories = ref([]); // 所有设定类别
const activeCategory = ref(''); // 当前选中的类别
const loreEntries = ref([]); // 当前类别下的所有设定条目

const formDialogVisible = ref(false);
const formRef = ref(null);
const isEditMode = computed(() => formData.id != null);
const availableKeysForCategory = computed(() => {
  if (activeCategory.value && allEnums[activeCategory.value]) {
    return allEnums[activeCategory.value];
  }
  return [];
});
const defaultFormData = () => ({
  id: null,
  category: activeCategory.value,
  key: '',
  name: '',
  description: '',
});
const formData = reactive(defaultFormData());
const formRules = {
  key: [{ required: true, message: '键 (Key) 不能为空', trigger: 'blur' }],
  name: [{ required: true, message: '名称不能为空', trigger: 'blur' }],
};

// --- 数据获取 ---
const fetchCategories = async () => {
  try {
    const response = await api.getEnums();
    // 将完整的枚举数据存入 allEnums
    Object.assign(allEnums, response.data);
    // 类别列表只取键名
    loreCategories.value = Object.keys(response.data);
    
    if (loreCategories.value.length > 0) {
      activeCategory.value = loreCategories.value[0];
      fetchLoreEntries();
    }
  } catch (error) {
    ElMessage.error("获取设定类别失败！");
  }
};

const fetchLoreEntries = async () => {
  if (!activeCategory.value) return;
  loading.value = true;
  try {
    const response = await api.getLoreEntries(activeCategory.value);
    loreEntries.value = response.data;
  } catch (error) {
    ElMessage.error(`获取 "${activeCategory.value}" 类别设定失败！`);
  } finally {
    loading.value = false;
  }
};

// --- 事件处理 ---
const handleCategorySelect = (category) => {
  activeCategory.value = category;
  fetchLoreEntries();
};

const resetForm = () => {
  Object.assign(formData, defaultFormData());
};

const handleOpenForm = (entry) => {
  resetForm();
  if (entry) { // 编辑模式
    Object.assign(formData, entry);
  }
  formDialogVisible.value = true;
};

const handleSubmit = async () => {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEditMode.value) {
          await api.updateLoreEntry(formData.id, formData);
          ElMessage.success("设定更新成功！");
        } else {
          await api.createLoreEntry(formData);
          ElMessage.success("新设定创建成功！");
        }
        formDialogVisible.value = false;
        fetchLoreEntries(); // 刷新列表
      } catch (error) {
        ElMessage.error("操作失败，请重试。");
      }
    }
  });
};

const handleDelete = async (entry) => {
  try {
    await ElMessageBox.confirm(`确定要删除设定 "${entry.name}" 吗？`, '警告', {
      type: 'warning'
    });
    await api.deleteLoreEntry(entry.id);
    ElMessage.success("删除成功！");
    fetchLoreEntries(); // 刷新列表
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error("删除失败，请重试。");
    }
  }
};

// --- 生命周期钩子 ---
onMounted(() => {
  fetchCategories();
});
</script>

<style scoped>
.lore-manager-container {
  padding: 0;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.form-tip {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  line-height: 1.5;
  margin-top: 4px;
}
</style>