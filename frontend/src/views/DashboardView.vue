<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card shadow="hover" class="welcome-card">
          <h1>欢迎来到角色管理面板</h1>
          <p>在这里，您可以总览、创建和管理您笔下的所有人物。</p>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="8">
        <el-card shadow="hover">
          <el-statistic title="已收录角色总数" :value="characterCount" />
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="8">
        <el-card shadow="hover">
          <el-statistic title="主要种族数量" :value="5">
            <template #suffix>
              <el-icon><i-ep-opportunity /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="8">
        <el-card shadow="hover">
          <el-statistic title="故事线" :value="1" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
// ref 和 onMounted 会被 unplugin-auto-import 自动导入，无需手动 import
import api from '../services/api';

// 创建一个响应式变量来存储角色数量
const characterCount = ref(0);

// 定义一个异步函数来获取数据
const fetchCharacterCount = async () => {
  try {
    const response = await api.getCharacters();
    // 将获取到的角色列表的长度赋值给 characterCount
    characterCount.value = response.data.length;
  } catch (error) {
    console.error("获取角色列表失败:", error);
    // 可以在这里使用 ElMessage 给出错误提示
  }
};

// 在组件挂载到 DOM 后，调用函数获取数据
onMounted(() => {
  fetchCharacterCount();
});
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;
  background-color: #f4f6f9;
  border: none;
}

.stats-row .el-card {
  text-align: center;
}

.el-statistic {
  --el-statistic-title-font-size: 16px;
}

h1 {
  margin: 0 0 10px;
  color: #303133;
}
</style>