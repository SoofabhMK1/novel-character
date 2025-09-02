<template>
  <div class="detail-container">
    <el-page-header @back="goBack" class="page-header">
      <template #content>
        <span class="text-large font-600 mr-3"> 角色详情 </span>
      </template>
    </el-page-header>

    <el-card v-if="character" shadow="never">
      <el-descriptions :column="3" border>
        <!-- 基础信息 -->
        <el-descriptions-item label="全名">{{ character.name }}</el-descriptions-item>
        <el-descriptions-item label="昵称">{{ character.nickname || '无' }}</el-descriptions-item>
        <el-descriptions-item label="年龄">{{ character.age || '未知' }}</el-descriptions-item>
        
        <el-descriptions-item label="种族">{{ character.race }}</el-descriptions-item>
        <el-descriptions-item label="性别">{{ character.gender }}</el-descriptions-item>
        <el-descriptions-item label="职业">{{ character.occupation || '无' }}</el-descriptions-item>

        <el-descriptions-item label="身高">{{ character.height_cm ? `${character.height_cm} cm` : '未知' }}</el-descriptions-item>
        <el-descriptions-item label="体型">{{ character.build }}</el-descriptions-item>
        <el-descriptions-item label="当前状态">{{ character.status }}</el-descriptions-item>
        
        <!-- 个性特征 -->
        <el-descriptions-item label="核心特质" :span="3">
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
        <el-descriptions-item label="优点">{{ character.personality_details.strengths || '无' }}</el-descriptions-item>
        <el-descriptions-item label="弱点" :span="3">{{ character.personality_details.weaknesses || '无' }}</el-descriptions-item>
        
        <!-- 背景故事 -->
        <el-descriptions-item label="家乡" :span="3">{{ character.background_details.hometown || '未知' }}</el-descriptions-item>
        <el-descriptions-item label="关键事件" :span="3">{{ character.background_details.key_life_events || '无' }}</el-descriptions-item>

      </el-descriptions>
    </el-card>

    <el-skeleton v-else :rows="10" animated />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../services/api';

// --- 获取路由信息 ---
const route = useRoute();
const router = useRouter();

// --- 响应式状态定义 ---
const character = ref(null);
const characterId = route.params.id; // 从 URL 中获取 :id 参数

// --- API 调用逻辑 ---
const fetchCharacterDetails = async () => {
  if (!characterId) return;

  try {
    const response = await api.getCharacter(characterId);
    character.value = response.data;
  } catch (error) {
    console.error(`获取ID为 ${characterId} 的角色详情失败:`, error);
    // 可以在这里添加错误处理，比如跳转到404页面
  }
};

// --- 事件处理 ---
const goBack = () => {
  router.push('/characters'); // 或者 router.back()
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
</style>