import axios from 'axios';
import _ from 'lodash';

// 创建一个 Axios 实例，我们可以为它设置一些默认值
const apiClient = axios.create({
  // 关键：在生产环境中，API 的基础 URL 就是当前域名下的 /api 路径
  // 在开发环境中，Vite 的代理会处理这个请求
  baseURL: '/api/v1', 
  headers: {
    'Content-Type': 'application/json',
  },
});

// 导出封装好的 API 请求函数
export default {

  // --- 新增：获取统计数据 ---
  getDashboardStats() {
    return apiClient.get('/characters/stats');
  },

  // 获取角色列表
  getCharacters({ skip = 0, limit = 100, sortBy = 'updated_at', order = 'desc' } = {}) {
    return apiClient.get(`/characters/?skip=${skip}&limit=${limit}&sort_by=${sortBy}&order=${order}`);
  },

  // 通过 ID 获取单个角色
  getCharacter(id) {
    return apiClient.get(`/characters/${id}`);
  },

  // 创建一个新角色
  createCharacter(characterData) {
    // 使用 lodash 的 pick 方法，只挑选出后端 CreateSchema 需要的字段
    const dataToSend = _.pick(characterData, [
      'name', 'nickname', 'age', 'gender', 'race', 'occupation',
      'height_cm', 'build', 'status', 'alignment', 'image_filename',
      'measurements', 'personality_details', 'appearance_details',
      'background_details', 'speech_patterns', 'bloodline'
    ]);
    return apiClient.post('/characters/', dataToSend);
  },

  updateCharacter(id, updateData) {
    // 对于更新，我们通常发送所有字段，但也可以进行净化
    // 关键是确保我们发送的是 image_filename 而不是 image_url
    const dataToSend = _.pick(updateData, [
      'name', 'nickname', 'age', 'gender', 'race', 'occupation',
      'height_cm', 'build', 'status', 'alignment', 'image_filename',
      'measurements', 'personality_details', 'appearance_details',
      'background_details', 'speech_patterns', 'bloodline'
    ]);
    return apiClient.put(`/characters/${id}`, dataToSend);
  },

  // 删除一个角色
  deleteCharacter(id) {
    return apiClient.delete(`/characters/${id}`);
  },

  // =======================================================
  // ==           新增：AI 生成 API 调用                ==
  // =======================================================
  generateCharacterFromPrompt(prompt, provider) {
    const requestData = {
      prompt: prompt,
      provider: provider
    };
    return apiClient.post('/ai/generate-character', requestData);
  },
  
    // =======================================================
    // ==           新增：角色关系 API 调用               ==
    // =======================================================

    getRelationships(characterId) {
      return apiClient.get(`/characters/${characterId}/relationships`);
    },

    addRelationship(characterFromId, relationshipData) {
      // relationshipData should be like { character_to_id, relationship_type, description }
      return apiClient.post(`/characters/${characterFromId}/relationships`, relationshipData);
    },

    deleteRelationship(relationshipId) {
      return apiClient.delete(`/characters/relationships/${relationshipId}`);
    },
  getFeatureFlags() {
    return apiClient.get('/utils/features');
  },
  getEnums() {
    return apiClient.get('/utils/enums');
  },
  getLoreEntries(category) {
    // 如果提供了 category，则按类别筛选
    if (category) {
      return apiClient.get(`/lore/?category=${category}`);
    }
    // 否则获取全部
    return apiClient.get('/lore/');
  },
};