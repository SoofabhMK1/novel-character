<template>
  <div class="form-container">
    <el-page-header @back="goBack" class="page-header">
      <template #content>
        <span class="text-large font-600 mr-3"> {{ pageTitle }} </span>
      </template>
    </el-page-header>

    <!-- ============================================== -->
    <!-- ==              AI 生成区域                 == -->
    <!-- ============================================== -->
    <el-card 
      v-if="aiGenerationEnabled" 
      shadow="never" 
      class="ai-generation-card"
      :class="selectedProviderTheme"
    >
      <template #header>
        <div class="card-header ai-header">
          <div class="ai-title">
            <strong>✨ AI 辅助创作</strong>
            <span>输入简单的想法，让 AI 帮助你构建角色。</span>
          </div>
          <!-- 服务商切换按钮组 -->
          <el-radio-group v-model="selectedProvider" size="small">
            <el-radio-button 
              v-for="provider in featureFlags.available_ai_providers"
              :key="provider"
              :label="provider"
            >
              {{ provider.toUpperCase() }}
            </el-radio-button>
          </el-radio-group>
        </div>
      </template>
      <el-input
        v-model="aiPrompt"
        type="textarea"
        :rows="3"
        placeholder="例如：一个厌倦了战争、隐居在深林中的年迈精灵德鲁伊"
        show-word-limit
        maxlength="200"
      />
      <div class="ai-actions">
        <!-- 移除代理 UI, 替换为信息提示 -->
        <el-alert 
          title="网络提示" 
          type="info" 
          show-icon 
          :closable="false"
          description="国内网络访问 Gemini 可能需要代理支持。"
          v-if="selectedProvider === 'gemini'"
          style="flex-grow: 1; margin-right: 15px; background-color: transparent;"
        />
        <div v-else style="flex-grow: 1;"></div>
        
        <el-button 
          type="primary" 
          @click="handleAIGenerate" 
          :loading="isGenerating"
          :color="selectedProvider === 'gemini' ? '#4285F4' : '#19c37d'"
        >
          {{ isGenerating ? '生成中...' : `使用 ${selectedProvider.toUpperCase()} 生成` }}
        </el-button>
      </div>
    </el-card>

    <el-card shadow="never" style="margin-top: 20px;">
      <el-form 
        ref="characterFormRef"
        :model="characterForm" 
        :rules="rules"
        label-width="100px"
        v-loading="loading"
      >
        <el-tabs v-model="activeTab">
          <!-- ============================================== -->
          <!-- ==        基础信息 Tab (补全字段)           == -->
          <!-- ============================================== -->
          <el-tab-pane label="基础信息" name="basic">
            <el-row :gutter="24">
              <el-col :xs="24" :sm="12">
                <el-form-item label="全名" prop="name">
                  <el-input v-model="characterForm.name" placeholder="请输入角色全名" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="昵称" prop="nickname">
                  <el-input v-model="characterForm.nickname" placeholder="角色的常用称呼" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                 <el-form-item label="种族" prop="race">
                  <el-select v-model="characterForm.race" placeholder="请选择种族" style="width: 100%;">
                    <el-option v-for="item in enums.Race" :key="item" :label="item" :value="item" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="职业" prop="occupation">
                  <el-input v-model="characterForm.occupation" placeholder="角色的职业" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="年龄" prop="age">
                  <el-input-number v-model="characterForm.age" :min="0" controls-position="right" style="width: 100%;"/>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="身高(cm)" prop="height_cm">
                  <el-input-number v-model="characterForm.height_cm" :min="0" controls-position="right" style="width: 100%;"/>
                </el-form-item>
              </el-col>
              <el-col :span="24">
                <el-form-item label="性别" prop="gender">
                  <el-radio-group v-model="characterForm.gender">
                    <el-radio v-for="item in enums.Gender" :key="item" :label="item" />
                  </el-radio-group>
                </el-form-item>
              </el-col>
            </el-row>
          </el-tab-pane>

          <!-- ============================================== -->
          <!-- ==       外貌与个性 Tab (补全字段)          == -->
          <!-- ============================================== -->
          <el-tab-pane label="外貌与个性" name="appearance">
            <el-row :gutter="24">
               <el-col :xs="24" :sm="12">
                <el-form-item label="体型" prop="build">
                  <el-select v-model="characterForm.build" placeholder="请选择体型" style="width: 100%;">
                    <el-option v-for="item in enums.BuildType" :key="item" :label="item" :value="item" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="阵营" prop="alignment">
                  <el-select v-model="characterForm.alignment" placeholder="请选择阵营" style="width: 100%;">
                    <el-option v-for="item in enums.Alignment" :key="item" :label="item" :value="item" />
                  </el-select>
                </el-form-item>
              </el-col>
               <el-col :span="24">
                 <el-form-item label="当前状态" prop="status">
                  <el-radio-group v-model="characterForm.status">
                    <el-radio v-for="item in enums.Status" :key="item" :label="item" />
                  </el-radio-group>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="血统" prop="bloodline">
                  <el-select v-model="characterForm.bloodline" placeholder="请选择血统" style="width: 100%;">
                    <el-option v-for="item in enums.Bloodline" :key="item" :label="item" :value="item" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="24">
                <el-form-item label="核心特质" prop="personality_details.core_traits">
                  <el-input v-model="coreTraitsInput" placeholder="特质之间用英文逗号 , 分隔" />
                </el-form-item>
              </el-col>
              <el-col :span="24">
                <el-form-item label="外貌描述" prop="appearance_details.description">
                  <el-input type="textarea" :rows="4" v-model="characterForm.appearance_details.description" placeholder="描述角色的外貌特征，如发色、瞳色、特殊标记等..." />
                </el-form-item>
              </el-col>
            </el-row>
          </el-tab-pane>
          <el-tab-pane label="背景故事" name="background">
             <el-form-item label="家乡" prop="background_details.hometown">
                <el-input v-model="characterForm.background_details.hometown" placeholder="角色长大的地方" />
             </el-form-item>
             <el-form-item label="关键事件" prop="background_details.key_life_events">
                <el-input type="textarea" :rows="4" v-model="characterForm.background_details.key_life_events" placeholder="描述塑造了角色的关键人生经历..." />
             </el-form-item>
          </el-tab-pane>
        </el-tabs> 
        <el-form-item class="form-actions">
          <el-button type="primary" @click="submitForm">保存角色</el-button>
          <el-button @click="goBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
// --- <script setup> 部分和上次完全一样，无需修改 ---
import { ref, onMounted, computed, watch, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import api from '../services/api';

const route = useRoute();
const router = useRouter();

const characterFormRef = ref(null);
const loading = ref(true);
const activeTab = ref('basic');
const characterId = ref(route.params.id || null);

// --- AI 相关状态 ---
const featureFlags = reactive({ available_ai_providers: [] });
const aiPrompt = ref('');
const isGenerating = ref(false);
const selectedProvider = ref(null); // 当前选中的服务商

// --- 计算属性 ---
const aiGenerationEnabled = computed(() => 
  featureFlags.available_ai_providers && featureFlags.available_ai_providers.length > 0
);
// 动态主题类
const selectedProviderTheme = computed(() => {
  if (!selectedProvider.value) return '';
  return `theme-${selectedProvider.value}`;
});

const isEditMode = computed(() => !!characterId.value);
const pageTitle = computed(() => isEditMode.value ? '编辑角色' : '新建角色');

const enums = reactive({ Gender: [], Race: [], Alignment: [], Status: [], BuildType: [] });

const defaultForm = () => ({
  name: '',
  nickname: '',
  age: null,
  gender: 'Other',
  race: 'Other',
  occupation: '',
  height_cm: null,
  build: 'Average',
  status: 'Unknown',
  bloodline: 'Unknown',
  alignment: 'True Neutral',
  personality_details: { core_traits: [] },
  appearance_details: { description: '' },
  background_details: { hometown: '', key_life_events: '' },
});
const characterForm = ref(defaultForm());
const coreTraitsInput = ref('');

const rules = {
  name: [{ required: true, message: '请输入角色全名', trigger: 'blur' }],
};

watch(() => characterForm.value.personality_details.core_traits, (newVal) => {
    coreTraitsInput.value = newVal ? newVal.join(', ') : '';
}, { deep: true });
watch(coreTraitsInput, (newVal) => {
    if (characterForm.value.personality_details) {
        characterForm.value.personality_details.core_traits = newVal ? newVal.split(',').map(t => t.trim()) : [];
    }
});

const fetchInitialData = async () => {
  loading.value = true;
  try {
    // 并行获取所有初始化数据
    const [enumsResponse, featuresResponse] = await Promise.all([
      api.getEnums(),
      api.getFeatureFlags()
    ]);

    Object.assign(enums, enumsResponse.data);
    Object.assign(featureFlags, featuresResponse.data);

    if (aiGenerationEnabled.value) {
      // 优先选择 deepseek，否则选择第一个可用的
      selectedProvider.value = featureFlags.available_ai_providers.includes('deepseek')
        ? 'deepseek'
        : featureFlags.available_ai_providers[0];
    }

    if (isEditMode.value) {
      const characterResponse = await api.getCharacter(characterId.value);
      characterForm.value = { ...defaultForm(), ...characterResponse.data };
    }
  } catch (error) {
    ElMessage.error('加载页面初始数据失败！');
    console.error(error);
  } finally {
    loading.value = false;
  }
};

// --- 逻辑处理 ---
const handleAIGenerate = async () => {
  if (!aiPrompt.value.trim()) {
    ElMessage.warning('请输入对角色的描述');
    return;
  }
  isGenerating.value = true;
  try {
    const response = await api.generateCharacterFromPrompt(
      aiPrompt.value,
      selectedProvider.value
    );
    // 用 AI 返回的数据覆盖表单，同时保留未生成字段的默认值
    characterForm.value = { ...defaultForm(), ...response.data };
    ElMessage.success('角色生成成功！请检查并完善细节。');
  } catch (error) {
    const errorMessage = error.response?.data?.detail || '生成失败，请检查网络或代理设置';
    ElMessage.error(errorMessage);
    console.error(error);
  } finally {
    isGenerating.value = false;
  }
};


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
        router.push('/characters');
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
  fetchInitialData();
});
</script>

<style scoped>
.form-container {
  padding: 0 24px 24px 24px;
}
.page-header {
  margin-bottom: 20px;
}
.form-actions {
  margin-top: 20px;
  /* 可以添加一些样式让它和 tabs 内容分开 */
  padding-top: 20px;
  border-top: 1px solid var(--el-border-color-lighter);
}
.ai-generation-card {
  transition: border-color 0.3s ease;
  border: 1px solid var(--el-border-color);
}
.ai-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.ai-title {
  display: flex;
  flex-direction: column;
}
.ai-title span {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-top: 4px;
}
.ai-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
}

/* --- 主题样式 --- */
.theme-gemini {
  border-color: #4285F4;
}
.theme-deepseek {
  border-color: #19c37d;
}
</style>