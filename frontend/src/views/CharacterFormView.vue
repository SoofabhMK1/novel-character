<template>
  <div class="form-container">
    <el-page-header @back="goBack" class="page-header">
      <template #content>
        <span class="text-large font-600 mr-3"> {{ pageTitle }} </span>
      </template>
    </el-page-header>

    <el-card shadow="never">
      <el-form 
        ref="characterFormRef"
        :model="characterForm" 
        :rules="rules"
        label-width="120px"
        v-loading="loading"
      >
        <el-tabs v-model="activeTab">
          <el-tab-pane label="基础信息" name="basic">
            <el-form-item label="全名" prop="name">
              <el-input v-model="characterForm.name" placeholder="请输入角色全名" />
            </el-form-item>
            <el-form-item label="昵称" prop="nickname">
              <el-input v-model="characterForm.nickname" placeholder="角色的常用称呼" />
            </el-form-item>
            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="characterForm.age" :min="0" />
            </el-form-item>
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="characterForm.gender">
                <el-radio label="Male">男</el-radio>
                <el-radio label="Female">女</el-radio>
                <el-radio label="Non-binary">非二元</el-radio>
                <el-radio label="Other">其他</el-radio>
              </el-radio-group>
            </el-form-item>
             <el-form-item label="职业" prop="occupation">
              <el-input v-model="characterForm.occupation" placeholder="角色的职业" />
            </el-form-item>
          </el-tab-pane>

          <el-tab-pane label="外貌与个性" name="appearance">
             <!-- 可以在这里添加更多表单项 -->
             <el-form-item label="核心特质" prop="personality_details.core_traits">
                <el-input v-model="coreTraitsInput" placeholder="特质之间用英文逗号 , 分隔" />
             </el-form-item>
          </el-tab-pane>
          
          <el-tab-pane label="背景故事" name="background">
             <!-- 可以在这里添加更多表单项 -->
          </el-tab-pane>
        </el-tabs>
        
        <el-form-item>
          <el-button type="primary" @click="submitForm">保存</el-button>
          <el-button @click="goBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import api from '../services/api';

const route = useRoute();
const router = useRouter();

// --- 状态定义 ---
const characterFormRef = ref(null);
const loading = ref(false);
const activeTab = ref('basic');
const characterId = ref(route.params.id || null);

const isEditMode = computed(() => !!characterId.value);
const pageTitle = computed(() => isEditMode.value ? '编辑角色' : '新建角色');

// --- 表单数据与规则 ---
const defaultForm = () => ({
  name: '',
  nickname: '',
  age: 0,
  gender: 'Other',
  occupation: '',
  personality_details: {
    core_traits: [],
  },
  // ... 其他字段的默认值
});
const characterForm = ref(defaultForm());
const coreTraitsInput = ref(''); // 用于绑定核心特质的输入框

const rules = {
  name: [{ required: true, message: '请输入角色全名', trigger: 'blur' }],
};

// --- 侦听器：同步核心特质输入框和表单数据 ---
watch(() => characterForm.value.personality_details.core_traits, (newVal) => {
    coreTraitsInput.value = newVal.join(', ');
});
watch(coreTraitsInput, (newVal) => {
    characterForm.value.personality_details.core_traits = newVal ? newVal.split(',').map(t => t.trim()) : [];
});

// --- 数据获取 (用于编辑模式) ---
const fetchCharacterData = async () => {
  if (!isEditMode.value) return;
  loading.value = true;
  try {
    const response = await api.getCharacter(characterId.value);
    characterForm.value = { ...defaultForm(), ...response.data };
  } catch (error) {
    ElMessage.error('加载角色数据失败！');
    console.error(error);
  } finally {
    loading.value = false;
  }
};

// --- 逻辑处理 ---
const submitForm = async () => {
  if (!characterFormRef.value) return;
  await characterFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      try {
        if (isEditMode.value) {
          await api.updateCharacter(characterId.value, characterForm.value);
          ElMessage.success('角色更新成功！');
        } else {
          await api.createCharacter(characterForm.value);
          ElMessage.success('角色创建成功！');
        }
        router.push('/characters'); // 成功后跳转到列表页
      } catch (error) {
        ElMessage.error('操作失败，请重试。');
        console.error(error);
      } finally {
        loading.value = false;
      }
    }
  });
};

const goBack = () => router.push('/characters');

onMounted(() => {
  fetchCharacterData();
});
</script>

<style scoped>
.form-container {
  padding: 0 24px 24px 24px;
}
.page-header {
  margin-bottom: 20px;
}
</style>