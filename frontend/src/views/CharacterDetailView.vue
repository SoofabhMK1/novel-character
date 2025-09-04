<template>
  <div class="detail-container">
    <el-page-header @back="goBack" class="page-header">
      <template #content>
        <span class="text-large font-600 mr-3"> 角色详情 </span>
      </template>
      <template #extra>
        <div class="action-buttons-header">
          <el-button @click="openRelationshipDialog">管理关系</el-button>
          <router-link :to="`/characters/${characterId}/edit`">
            <el-button type="primary">编辑</el-button>
          </router-link>
        </div>
      </template>
    </el-page-header>

    <!-- ============================================== -->
    <!-- ==      关键修正：确保所有内容都在 Card 内部    == -->
    <!-- ============================================== -->
    <div v-if="character" class="detail-layout-grid">
      
      <!-- 区域一：左上角 - 角色形象 -->
      <div class="character-image-card">
        <el-card shadow="never">
          <template #header><strong>角色形象</strong></template>
          <el-image 
            v-if="character.image_url"
            :src="character.image_url" 
            fit="cover"
            class="character-image"
            :preview-src-list="[character.image_url]" 
            preview-teleported
          >
             <!-- ... (error slot) ... -->
          </el-image>
          <el-empty v-else description="暂无图片" />
        </el-card>
      </div>

      <!-- 区域二：右上角 - 核心信息 -->
      <div class="core-info-card">
        <el-card shadow="never">
          <template #header><strong>核心档案</strong></template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="全名">{{ character.name }}</el-descriptions-item>
            <el-descriptions-item label="昵称">{{ character.nickname || '无' }}</el-descriptions-item>
            <el-descriptions-item label="种族">
              <el-link type="primary" @click="showLore('Race', character.race)">{{ character.race }}</el-link>
            </el-descriptions-item>
            <el-descriptions-item label="职业">{{ character.occupation || '无' }}</el-descriptions-item>
            <el-descriptions-item label="阵营">
              <el-link type="primary" @click="showLore('Alignment', character.alignment)">{{ character.alignment }}</el-link>
            </el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-link type="primary" @click="showLore('Status', character.status)">{{ character.status }}</el-link>
            </el-descriptions-item>
            <el-descriptions-item label="血统">{{ character.bloodline }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </div>

      <!-- 区域三：下方整行 - 详细资料 (使用 Tabs) -->
      <div class="detailed-info-card">
        <el-card shadow="never">
          <el-tabs type="border-card">
            <el-tab-pane label="个性特征">
              <el-descriptions :column="1" border>
                <el-descriptions-item label="核心特质">
                  <el-tag v-for="trait in character.personality_details.core_traits" :key="trait" class="trait-tag" effect="plain">{{ trait }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="MBTI">{{ character.personality_details.mbti || '未设定' }}</el-descriptions-item>
                <el-descriptions-item label="优点">{{ character.personality_details.strengths || '无' }}</el-descriptions-item>
                <el-descriptions-item label="弱点">{{ character.personality_details.weaknesses || '无' }}</el-descriptions-item>
              </el-descriptions>
            </el-tab-pane>
            <el-tab-pane label="生理特征">
               <el-descriptions :column="1" border>
                <el-descriptions-item label="年龄">{{ character.age || '未知' }}</el-descriptions-item>
                <el-descriptions-item label="身高">{{ character.height_cm ? `${character.height_cm} cm` : '未知' }}</el-descriptions-item>
                <el-descriptions-item label="体型">{{ character.build }}</el-descriptions-item>
                <el-descriptions-item label="性别">{{ character.gender }}</el-descriptions-item>
            <el-descriptions-item label="尺寸">
              {{ formattedMeasurements }}
            </el-descriptions-item>
            <el-descriptions-item label="特征">{{ character.appearance_details.distinguishing_features }}</el-descriptions-item>
            <!-- <el-descriptions-item label="当前状态">{{ character.status }}</el-descriptions-item> -->
            </el-descriptions>
            </el-tab-pane>
            <el-tab-pane label="背景故事">
              <el-descriptions :column="1" border>
                <el-descriptions-item label="家乡">{{ character.background_details.hometown || '未知' }}</el-descriptions-item>
                <el-descriptions-item label="关键事件">{{ character.background_details.key_life_events || '无' }}</el-descriptions-item>
              </el-descriptions>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </div>

    </div>

    <el-skeleton v-else :rows="10" animated />

    <!-- ============================================== -->
    <!-- ==         新增：设定详情模态框             == -->
    <!-- ============================================== -->
    <el-dialog
      v-model="loreDialogVisible"
      :title="currentLoreEntry?.name || '设定详情'"
      width="50%"
    >
      <div v-if="currentLoreEntry">
        <p style="white-space: pre-wrap;">{{ currentLoreEntry.description }}</p>
        <el-divider />
        <div v-if="currentLoreEntry.attributes && Object.keys(currentLoreEntry.attributes).length > 0">
          <strong>附加属性:</strong>
          <ul>
            <li v-for="(value, key) in currentLoreEntry.attributes" :key="key">
              <strong>{{ key }}:</strong> {{ Array.isArray(value) ? value.join(', ') : value }}
            </li>
          </ul>
        </div>
      </div>
      <el-empty v-else description="暂无该设定的详细信息。" />
    </el-dialog>

    <!-- 关系管理模态框 (保持不变) -->
    <el-dialog
      v-model="relationshipDialogVisible"
      :title="`管理 '${character?.name}' 的人际关系`"
      width="70%"
      @close="resetNewRelationship"
    >
      <!-- 添加新关系表单 -->
      <el-card shadow="never" class="add-relationship-card">
        <template #header><strong>添加新关系</strong></template>
        <el-form :model="newRelationship" label-width="80px" inline class="relationship-form">
          <el-form-item label="目标角色">
            <el-select
              v-model="newRelationship.character_to_id"
              placeholder="选择一个角色"
              filterable
            >
              <el-option
                v-for="char in otherCharacters"
                :key="char.id"
                :label="char.name"
                :value="char.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="关系类型">
            <el-select v-model="newRelationship.relationship_type" 
              placeholder="选择关系"
              class="form-select"
            >
              <el-option
                v-for="relType in enums.RelationshipType"
                :key="relType"
                :label="relType"
                :value="relType"
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleAddRelationship">添加</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 关系列表 -->
      <el-table :data="relationships" v-loading="loadingRelationships" style="margin-top: 20px;">
        <el-table-column label="关系描述">
          <template #default="scope">
            <div class="relationship-cell">
              <strong class="character-name">{{ getRelationSubject(scope.row) }}</strong>
              <span class="relation-text">是</span>
              <el-tag>{{ scope.row.relationship_type }}</el-tag>
              <span class="relation-text">对于</span>
              <strong class="character-name">{{ getRelationObject(scope.row) }}</strong>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" align="center">
          <template #default="scope">
            <el-button 
              type="danger" 
              link 
              @click="handleDeleteRelationship(scope.row.id)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="relationshipDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';
import { Picture as IconPicture } from '@element-plus/icons-vue';
import { ElMessage, ElMessageBox } from 'element-plus';

// --- 基础状态和路由 ---
const route = useRoute();
const router = useRouter();
const character = ref(null);
const characterId = route.params.id;

// --- 新增：设定集相关的状态 ---
const loreData = reactive({}); // 用于缓存所有设定数据
const loreDialogVisible = ref(false);
const currentLoreEntry = ref(null);

// --- 关系模态框状态 ---
const relationshipDialogVisible = ref(false);
const loadingRelationships = ref(false);
const relationships = ref([]);
const otherCharacters = ref([]);
const enums = reactive({ RelationshipType: [] });
const newRelationship = reactive({
  character_to_id: '',
  relationship_type: '',
});

const formattedMeasurements = computed(() => {
  // 关键：检查 character 和 measurements 是否存在，防止在数据加载完成前报错
  if (!character.value || !character.value.measurements) {
    return '—'; // 或者返回 '无数据'
  }

  // 获取 measurements 对象
  const measurements = character.value.measurements;
  const measurementLabels = {
    bust_cm: '胸围',
    waist_cm: '腰围',
    hip_cm: '臀围'
  };
  // 将对象转换为 "Key: Value" 格式的字符串数组
  // Object.entries({ "胸围": 88, "腰围": 57 }) -> [ ['胸围', 88], ['腰围', 57] ]
  const parts = Object.entries(measurements).map(([key, value]) => {
    return `${measurementLabels[key]}: ${value}`; // -> "胸围: 88"
  });

  // 使用 ' / ' 将数组元素连接成一个最终的字符串
  // -> "胸围: 88 / 腰围: 57 / 臀围: 86"
  return parts.join(' / ');
});

// --- 数据获取 ---
const fetchCharacterDetails = async () => {
  if (!characterId) return;
  
  // =======================================================
  // ==        为核心数据获取添加 try...catch           ==
  // =======================================================
  try {
    const response = await api.getCharacter(characterId);
    character.value = response.data;
  } catch (error) {
    console.error(`获取ID为 ${characterId} 的角色详情失败:`, error);
    // 给用户一个清晰的反馈
    ElMessage.error('加载角色详情失败，请检查网络或联系管理员。');
    // （可选）可以跳转到错误页面或列表页
    // router.push('/characters'); 
  }
};

// --- 新增：获取所有设定数据 ---
const fetchAllLoreData = async () => {
  try {
    // 一次性获取所有设定
    const response = await api.getLoreEntries();
    // 将返回的数组按 category 分组，方便查找
    for (const entry of response.data) {
      if (!loreData[entry.category]) {
        loreData[entry.category] = {};
      }
      loreData[entry.category][entry.key] = entry;
    }
  } catch (error) {
    console.error("获取世界观设定集失败:", error);
    ElMessage.error("获取世界观设定集失败！");
  }
};

// --- 新增：显示设定详情的函数 ---
const showLore = (category, key) => {
  if (!key) {
    currentLoreEntry.value = null;
    loreDialogVisible.value = true;
    return;
  }
  
  // 直接使用原始的、大小写敏感的 key 进行查找
  const entry = loreData[category]?.[key];
  
  if (entry) {
    currentLoreEntry.value = entry;
  } else {
    // 这个 log 现在非常有用，能立刻告诉我们哪个 key 不匹配
    console.error(`Key '${key}' not found in category '${category}'.`);
    currentLoreEntry.value = null;
  }
  
  loreDialogVisible.value = true;
};
const fetchRelationshipData = async () => {
  if (!characterId) return;
  loadingRelationships.value = true;
  try {
    const [relsResponse, allCharsResponse, enumsResponse] = await Promise.all([
      api.getRelationships(characterId),
      api.getCharacters({ limit: 1000 }),
      api.getEnums()
    ]);
    
    relationships.value = relsResponse.data;
    otherCharacters.value = allCharsResponse.data.filter(c => c.id !== characterId);
    enums.RelationshipType = enumsResponse.data.RelationshipType;
  } catch (error) {
    console.error("加载关系数据失败:", error);
    ElMessage.error('加载关系数据失败！');
  } finally {
    loadingRelationships.value = false;
  }
};

// --- 事件处理 ---
const goBack = () => router.push('/characters');

const openRelationshipDialog = () => {
  relationshipDialogVisible.value = true;
  fetchRelationshipData(); // 打开时加载数据
};

const resetNewRelationship = () => {
  newRelationship.character_to_id = '';
  newRelationship.relationship_type = '';
};

const handleAddRelationship = async () => {
  if (!newRelationship.character_to_id || !newRelationship.relationship_type) {
    ElMessage.warning('请选择目标角色和关系类型');
    return;
  }
  try {
    await api.addRelationship(characterId, newRelationship);
    ElMessage.success('关系添加成功！');
    resetNewRelationship();
    fetchRelationshipData(); // 重新加载列表
  } catch (error) {
    console.error("添加关系失败:", error);
    ElMessage.error('添加关系失败！');
  }
};

const handleDeleteRelationship = async (relationshipId) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这条关系吗？此操作不可撤销。',
      '警告',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );
    // 用户点击了确认
    await api.deleteRelationship(relationshipId);
    ElMessage.success('关系已删除');
    fetchRelationshipData(); // 重新加载列表
  } catch (action) {
    // 用户点击了取消或关闭对话框
    if (action === 'cancel') {
      ElMessage.info('操作已取消');
    }
  }
};

// --- 辅助计算属性 (用于清晰展示双向关系) ---
const getRelationshipLabel = (row) => {
  // 判断当前查看的角色是不是关系的发起方
  const isSubject = row.character_from.id === characterId;
  // 如果是发起方，使用正向描述；否则，使用反向描述。
  return isSubject ? row.perspective_label : row.inverse_perspective_label;
};

const getRelationSubject = (row) => {
  // 现在这个函数需要处理反转情况
  const isSubject = row.character_from.id === characterId;
  return isSubject ? '你' : row.character_from.name;
};
const getRelationObject = (row) => {
  const isSubject = row.character_from.id === characterId;
  return isSubject ? row.character_to.name : '你';
};

// --- 生命周期钩子 ---
onMounted(() => {
  Promise.all([
    fetchCharacterDetails(),
    fetchAllLoreData()
  ]);
});
</script>

<style scoped>
/* ======================================================= */
/* ==                主容器与页头样式                   == */
/* ======================================================= */
.detail-container {
  /* 移除左右 padding，因为 main-content-wrapper 已经提供了 */
  padding: 0; 
}

.page-header {
  margin-bottom: 24px;
}

.action-buttons-header {
  display: flex;
  gap: 10px;
}

/* ======================================================= */
/* ==            最终的 CSS Grid 布局样式             == */
/* ======================================================= */
.detail-layout-grid {
  display: grid;
  /* 定义两列，左列是图片的宽度，右列占据剩余空间 */
  grid-template-columns: 320px 1fr;
  /* 定义行和列的间距 */
  gap: 24px;
}

/* 定义每个区域在网格中的位置 */
.character-image-card {
  grid-column: 1 / 2; /* 占据第 1 列 */
  grid-row: 1;      /* 占据第 1 行 */
}

.core-info-card {
  grid-column: 2 / 3; /* 占据第 2 列 */
  grid-row: 1;      /* 占据第 1 行 */
}

.detailed-info-card {
  grid-column: 1 / 3; /* 横跨两列 */
  grid-row: 2;      /* 占据第 2 行 */
}

/* ======================================================= */
/* ==                卡片内部元素样式                   == */
/* ======================================================= */
.character-image {
  width: 100%;
  height: 400px; /* 可以根据喜好调整 */
  border-radius: 4px;
  background-color: #f5f7fa;
}

.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
  font-size: 30px;
}

.trait-tag {
  margin-right: 8px;
  margin-bottom: 8px; /* 用于在换行时提供垂直间距 */
}

/* ======================================================= */
/* ==                关系管理模态框样式                 == */
/* ======================================================= */
.add-relationship-card {
  margin-bottom: 20px;
  background-color: #fafafa;
  border-radius: 4px;
}

.relationship-form {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 15px;
}

.relationship-form .el-form-item {
  margin-bottom: 0;
}

.form-select {
  width: 220px;
}

.relationship-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.character-name {
  color: var(--el-color-primary);
  font-weight: bold;
}


/* ======================================================= */
/* ==                 响应式设计 (小屏幕)               == */
/* ======================================================= */
@media (max-width: 992px) { /* 在平板尺寸时触发 */
  .detail-layout-grid {
    grid-template-columns: 1fr; /* 变为一列 */
  }
  .character-image-card,
  .core-info-card,
  .detailed-info-card {
    grid-column: 1; /* 所有项都占据唯一的列 */
  }
  .core-info-card {
    grid-row: 2;
  }
  .detailed-info-card {
    grid-row: 3;
  }
}
</style>