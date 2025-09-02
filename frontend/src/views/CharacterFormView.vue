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
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="全名" prop="name">
                  <el-input v-model="characterForm.name" placeholder="请输入角色全名" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="昵称" prop="nickname">
                  <el-input v-model="characterForm.nickname" placeholder="角色的常用称呼" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                 <el-form-item label="种族" prop="race">
                  <el-select v-model="characterForm.race" placeholder="请选择种族" style="width: 100%;">
                    <el-option v-for="item in enums.Race" :key="item" :label="item" :value="item" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="职业" prop="occupation">
                  <el-input v-model="characterForm.occupation" placeholder="角色的职业" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="年龄" prop="age">
                  <el-input-number v-model="characterForm.age" :min="0" />
                </el-form-item>
              </el-col>
               <el-col :span="12">
                <el-form-item label="性别" prop="gender">
                  <el-radio-group v-model="characterForm.gender">
                    <el-radio v-for="item in enums.Gender" :key="item" :label="item" />
                  </el-radio-group>
                </el-form-item>
              </el-col>
            </el-row>
          </el-tab-pane>

          <el-tab-pane label="外貌与个性" name="appearance">
             <el-form-item label="核心特质" prop="personality_details.core_traits">
                <el-input v-model="coreTraitsInput" placeholder="特质之间用英文逗号 , 分隔" />
             </el-form-item>
             <el-form-item label="外貌描述" prop="appearance_details.description">
                <el-input type="textarea" :rows="4" v-model="characterForm.appearance_details.description" placeholder="描述角色的外貌特征..." />
             </el-form-item>
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
        
        <!-- ======================================================= -->
        <!-- == 关键修正：确保这个 el-form-item 在 </el-tabs> 之后 == -->
        <!-- ======================================================= -->
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

const isEditMode = computed(() => !!characterId.value);
const pageTitle = computed(() => isEditMode.value ? '编辑角色' : '新建角色');

const enums = reactive({ Gender: [], Race: [], Alignment: [], Status: [], BuildType: [] });

const defaultForm = () => ({
  name: '',
  nickname: '',
  age: 0,
  gender: 'Other',
  race: 'Other',
  occupation: '',
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
    const enumsResponse = await api.getEnums();
    Object.assign(enums, enumsResponse.data);
    if (isEditMode.value) {
      const characterResponse = await api.getCharacter(characterId.value);
      characterForm.value = { ...defaultForm(), ...characterResponse.data };
    }
  } catch (error) {
    ElMessage.error('加载初始数据失败！');
    console.error(error);
  } finally {
    loading.value = false;
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
</style>