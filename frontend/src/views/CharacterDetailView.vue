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
    <el-card v-if="character" shadow="never">
      <el-row :gutter="30">
        <!-- 左侧：描述列表 -->
        <el-col :xs="24" :md="16">
          <el-descriptions :column="2" border>
            <!-- 基础信息 -->
            <el-descriptions-item label="全名">{{ character.name }}</el-descriptions-item>
            <el-descriptions-item label="昵称">{{ character.nickname || '无' }}</el-descriptions-item>
            <el-descriptions-item label="年龄">{{ character.age || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="种族">{{ character.race }}</el-descriptions-item>
            <el-descriptions-item label="性别">{{ character.gender }}</el-descriptions-item>
            <el-descriptions-item label="职业">{{ character.occupation || '无' }}</el-descriptions-item>
            <el-descriptions-item label="身高">{{ character.height_cm ? `${character.height_cm} cm` : '未知' }}</el-descriptions-item>
            <el-descriptions-item label="体型">{{ character.build }}</el-descriptions-item>
            <el-descriptions-item label="尺寸">
              {{ formattedMeasurements }}
            </el-descriptions-item>
            <el-descriptions-item label="当前状态">{{ character.status }}</el-descriptions-item>
            
            <!-- 个性特征 -->
            <el-descriptions-item label="核心特质" :span="2">
              <el-tag 
                v-for="trait in character.personality_details.core_traits" 
                :key="trait"
                class="trait-tag"
                effect="plain"
              >
                {{ trait }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="阵营">{{ character.alignment }}</el-descriptions-item>
            <el-descriptions-item label="MBTI">{{ character.personality_details.mbti || '未设定' }}</el-descriptions-item>
            <el-descriptions-item label="优点" :span="2">{{ character.personality_details.strengths || '无' }}</el-descriptions-item>
            <el-descriptions-item label="弱点" :span="2">{{ character.personality_details.weaknesses || '无' }}</el-descriptions-item>
            
            <!-- 背景故事 -->
            <el-descriptions-item label="家乡" :span="2">{{ character.background_details.hometown || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="关键事件" :span="2">{{ character.background_details.key_life_events || '无' }}</el-descriptions-item>
          </el-descriptions>
        </el-col>

        <!-- 右侧：角色图片 -->
        <el-col :xs="24" :md="8">
          <el-image 
            v-if="character.image_url"
            :src="character.image_url" 
            fit="contain"
            class="character-image"
          >
            <template #error>
              <div class="image-slot">
                <el-icon><icon-picture /></el-icon>
              </div>
            </template>
          </el-image>
          <el-empty v-else description="暂无图片" />
        </el-col>
      </el-row>
    </el-card>

    <el-skeleton v-else :rows="10" animated />

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

  // 将对象转换为 "Key: Value" 格式的字符串数组
  // Object.entries({ "胸围": 88, "腰围": 57 }) -> [ ['胸围', 88], ['腰围', 57] ]
  const parts = Object.entries(measurements).map(([key, value]) => {
    return `${key}: ${value}`; // -> "胸围: 88"
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
  fetchCharacterDetails();
});
</script>

<style scoped>
.detail-container {
  padding: 0 24px 24px 24px;
}
.page-header {
  margin-bottom: 20px;
}
.trait-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}
.character-image {
  width: 100%;
  height: 400px; /* 给一个固定高度 */
  background-color: #f5f7fa;
  border-radius: 4px;
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
.action-buttons-header {
  display: flex;
  gap: 10px;
}
.add-relationship-card {
  margin-bottom: 20px;
}
.relationship-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}
.character-name {
  color: var(--el-color-primary);
}
.relationship-form {
  display: flex;
  flex-wrap: wrap; /* 允许换行 */
  gap: 10px;
}

.relationship-form .el-form-item {
  margin-bottom: 0; /* inline 模式下不需要底部 margin */
}

.form-select {
  width: 200px; /* 给下拉框一个固定的、足够的宽度 */
}

</style>