<template>
  <div class="character-list-container">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>角色列表</span>
          <el-button type="primary">+ 新建角色</el-button>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="characters"
        style="width: 100%"
        border
        stripe
      >
        <el-table-column prop="name" label="姓名" width="180" />
        <el-table-column prop="race" label="种族" width="120" />
        <el-table-column prop="occupation" label="职业" />
        <el-table-column prop="status" label="状态" width="120" />
        <el-table-column fixed="right" label="操作" width="150">
          <template #default>
            <el-button type="primary" link size="small">编辑</el-button>
            <el-button type="danger" link size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页组件 -->
      <el-pagination
        v-if="total > 0"
        background
        layout="prev, pager, next, total"
        :total="total"
        :page-size="pageSize"
        @current-change="handlePageChange"
        class="pagination-container"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';

// --- 响应式状态定义 ---
const characters = ref([]);
const loading = ref(true); // 控制加载状态
const total = ref(0); // 角色总数，用于分页
const currentPage = ref(1);
const pageSize = ref(10); // 每页显示10条

// --- API 调用逻辑 ---
const fetchCharacters = async () => {
  loading.value = true;
  try {
    const skip = (currentPage.value - 1) * pageSize.value;
    const response = await api.getCharacters({
      skip: skip,
      limit: pageSize.value,
      sortBy: 'name', // 按名字升序排列
      order: 'asc'
    });
    characters.value = response.data;
    // 注意：后端目前没有返回总数，我们暂时用返回的数组长度。
    // 一个更优的方案是让后端API返回总数。
    // 为了让分页正常工作，我们需要先获取一次所有数据来得到总数。
    if (total.value === 0) {
      const allCharactersResponse = await api.getCharacters({ limit: 1000 }); // 获取一个较大的数量来模拟获取总数
      total.value = allCharactersResponse.data.length;
    }
  } catch (error) {
    console.error("获取角色列表失败:", error);
  } finally {
    loading.value = false;
  }
};

// --- 事件处理 ---
const handlePageChange = (newPage) => {
  currentPage.value = newPage;
  fetchCharacters();
};

// --- 生命周期钩子 ---
onMounted(() => {
  fetchCharacters();
});
</script>

<style scoped>
.character-list-container {
  padding: 0; /* 主布局已经有 padding */
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>