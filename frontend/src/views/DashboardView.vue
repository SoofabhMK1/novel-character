<template>
  <div class="dashboard-container">
    <!-- 欢迎区 -->
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card shadow="never" class="welcome-card">
          <h1>欢迎回来，创作者！</h1>
          <p>你的世界正在等待被书写。今天准备为哪个角色注入新的活力？</p>
        </el-card>
      </el-col>
    </el-row>

    <!-- 数据统计区 -->
    <el-row v-if="stats" :gutter="20" class="stats-row">
      <el-col :xs="12" :sm="12" :md="6">
        <el-card shadow="hover">
          <el-statistic title="角色总数" :value="stats.total_characters" />
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="12" :md="6">
        <el-card shadow="hover">
          <el-statistic title="存活角色" :value="stats.alive_characters" />
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="12" :md="6">
        <el-card shadow="hover">
          <el-statistic title="善良阵营" :value="stats.good_alignment_count" />
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="12" :md="6">
        <el-card shadow="hover">
          <el-statistic title="已定义关系" :value="stats.total_relationships" />
        </el-card>
      </el-col>
    </el-row>
    <el-skeleton v-else :rows="2" animated />

    <!-- 快捷工作区 -->
    <el-row :gutter="20">
      <!-- 左侧：最近编辑 -->
      <el-col :xs="24" :md="16">
        <el-card shadow="hover" class="workspace-card">
          <template #header>
            <div class="card-header">
              <span>最近动向</span>
            </div>
          </template>
          <el-table v-if="recentCharacters.length > 0" :data="recentCharacters" style="width: 100%">
            <el-table-column prop="name" label="角色名" />
            <el-table-column prop="updated_at" label="上次编辑时间">
              <template #default="scope">
                <span>{{ formatTimeAgo(scope.row.updated_at) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template #default>
                <el-button type="primary" link>查看详情</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-empty v-else description="暂无角色，快去创建你的第一个角色吧！" />
        </el-card>
      </el-col>

      <!-- 右侧：快捷操作 -->
      <el-col :xs="24" :md="8">
        <el-card shadow="hover" class="workspace-card">
          <template #header>
            <div class="card-header">
              <span>快速开始</span>
            </div>
          </template>
          <div class="quick-actions">
            <el-button type="primary" size="large" style="width: 100%;">+ 新建角色</el-button>
            <el-button size="large" style="width: 100%; margin-top: 10px;">查看所有角色</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
// 引入一个时间格式化库会更方便，但这里我们先用一个简单的函数
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';


// --- 响应式状态定义 ---
const stats = ref(null);
const recentCharacters = ref([]);

// --- API 调用逻辑 ---
const fetchData = async () => {
  try {
    // 并行获取所有数据
    const [statsResponse, recentCharactersResponse] = await Promise.all([
      api.getDashboardStats(),
      api.getCharacters({ limit: 5, sortBy: 'updated_at', order: 'desc' })
    ]);
    stats.value = statsResponse.data;
    recentCharacters.value = recentCharactersResponse.data;
  } catch (error) {
    console.error("获取仪表盘数据失败:", error);
    // 这里可以使用 ElMessage 提示用户
  }
};

// --- 辅助函数 ---
const formatTimeAgo = (dateString) => {
  if (!dateString) return '';
  return formatDistanceToNow(new Date(dateString), { addSuffix: true, locale: zhCN });
};

// --- 生命周期钩子 ---
onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.dashboard-container {
  padding: 24px;
}
.welcome-card {
  margin-bottom: 20px;
  border: none;
}
.stats-row {
  margin-bottom: 20px;
}
.stats-row .el-card {
  text-align: center;
}
.workspace-card {
  height: 100%;
}
.card-header {
  font-weight: bold;
}
.quick-actions .el-button {
  margin-left: 0 !important;
}
</style>```

**为了使用 `formatDistanceToNow`，你需要安装 `date-fns` 库：**
```bash
# 在 frontend 目录下运行
npm install date-fns