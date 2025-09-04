<template>
  <div class="lore-manager-container">
    <el-row :gutter="24">
      <!-- 左侧：类别导航 -->
      <el-col :xs="24" :sm="8" :md="6">
        <el-card class="category-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><Reading /></el-icon>
              <strong>设定类别</strong>
            </div>
          </template>
          <el-menu
            :default-active="activeCategory"
            @select="handleCategorySelect"
            class="category-menu"
          >
            <el-menu-item
              v-for="category in loreCategories"
              :key="category"
              :index="category"
            >
              <el-icon><CollectionTag /></el-icon>
              <span>{{ category }}</span>
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>

      <!-- 右侧：数据表格与操作 -->
      <el-col :xs="24" :sm="16" :md="18">
        <el-card class="entries-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <div class="header-left">
                <el-icon><MessageBox /></el-icon>
                <span>{{ activeCategory }} - 设定列表</span>
              </div>
              <el-button type="primary" :icon="Plus" @click="handleOpenForm(null)">新建设定</el-button>
            </div>
          </template>
          
          <el-table :data="loreEntries" v-loading="loading" border stripe height="calc(100vh - 260px)">
            <el-table-column prop="key" label="键 (Key)" width="200">
               <template #default="scope">
                <el-tag>{{ scope.row.key }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="名称" width="200" />
            <el-table-column prop="description" label="描述" show-overflow-tooltip />
            <el-table-column label="操作" width="120" fixed="right" align="center">
              <template #default="scope">
                <el-tooltip content="编辑" placement="top">
                  <el-button link type="primary" :icon="Edit" @click="handleOpenForm(scope.row)" />
                </el-tooltip>
                <el-tooltip content="删除" placement="top">
                  <el-button link type="danger" :icon="Delete" @click="handleDelete(scope.row)" />
                </el-tooltip>
              </template>
            </el-table-column>
            <!-- 自定义空状态 -->
            <template #empty>
              <el-empty description="暂无设定，快去创建一条吧！">
                <el-button type="primary" :icon="Plus" @click="handleOpenForm(null)">立即创建</el-button>
              </el-empty>
            </template>
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
      top="8vh"
    >
      <template #header="{ close, titleId, titleClass }">
        <div class="dialog-header">
          <el-icon v-if="isEditMode"><Edit /></el-icon>
          <el-icon v-else><CirclePlus /></el-icon>
          <span :id="titleId" :class="titleClass">{{ isEditMode ? `编辑设定: ${formData.name}` : `新建设定 - ${activeCategory}` }}</span>
        </div>
      </template>

      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px" style="padding: 0 20px;">
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
            "键"是与程序枚举对应的唯一标识，创建后不可修改。
          </div>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="formData.name" placeholder="例如：人类 / Human" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" :rows="4" v-model="formData.description" placeholder="请详细描述该设定的背景、特点等。" />
        </el-form-item>
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
// 引入所需图标
import {
  CollectionTag,
  Plus,
  Edit,
  Delete,
  Reading,
  MessageBox,
  CirclePlus
} from '@element-plus/icons-vue';

// --- 状态定义 ---
const allEnums = reactive({});
const loading = ref(false);
const loreCategories = ref([]);
const activeCategory = ref('');
const loreEntries = ref([]);

const formDialogVisible = ref(false);
const formRef = ref(null);
const isEditMode = computed(() => formData.id != null);
const availableKeysForCategory = computed(() => {
  if (activeCategory.value && allEnums[activeCategory.value]) {
    // 过滤掉已经被使用的 key
    const usedKeys = loreEntries.value.map(entry => entry.key);
    return allEnums[activeCategory.value].filter(key => !usedKeys.includes(key));
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
  key: [{ required: true, message: '键 (Key) 不能为空', trigger: 'change' }], // trigger 改为 change
  name: [{ required: true, message: '名称不能为空', trigger: 'blur' }],
};

// --- 数据获取 ---
const fetchCategories = async () => {
  try {
    const response = await api.getEnums();
    Object.assign(allEnums, response.data);
    loreCategories.value = Object.keys(response.data);
    
    if (loreCategories.value.length > 0 && !activeCategory.value) {
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
        fetchLoreEntries();
      } catch (error) {
        ElMessage.error(error.response?.data?.message || "操作失败，请重试。");
      }
    }
  });
};

const handleDelete = async (entry) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除设定 "<strong>${entry.name}</strong>" 吗？此操作不可恢复。`, 
      '警告', 
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        dangerouslyUseHTMLString: true, // 允许在消息中使用 HTML
        icon: Delete,
      }
    );
    await api.deleteLoreEntry(entry.id);
    ElMessage.success("删除成功！");
    fetchLoreEntries();
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
  padding: 20px; /* 增加整体内边距 */
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
}

.card-header .el-icon {
  margin-right: 8px;
  vertical-align: middle;
}

.header-left {
  display: flex;
  align-items: center;
}

.category-card, .entries-card {
  height: calc(100vh - 145px); /* 计算卡片高度以适应视口 */
  display: flex;
  flex-direction: column;
}

.entries-card .el-card__body {
  flex: 1;
  overflow: hidden;
}

.category-menu {
  border-right: none; /* 移除菜单右边框 */
}

.category-menu .el-menu-item {
  transition: background-color 0.2s, color 0.2s;
}

.category-menu .el-menu-item.is-active {
  background-color: var(--el-color-primary-light-9);
  font-weight: bold;
}

.form-tip {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  line-height: 1.5;
  margin-top: 4px;
}

.el-table .el-button {
  font-size: 16px; /* 放大操作图标 */
  margin: 0 4px;
}

.dialog-header {
  display: flex;
  align-items: center;
  font-size: 18px;
  color: var(--el-text-color-primary);
}
.dialog-header .el-icon {
  margin-right: 10px;
}
</style>