import axios from 'axios';

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
    return apiClient.post('/characters/', characterData);
  },

  // 更新一个角色
  updateCharacter(id, updateData) {
    return apiClient.put(`/characters/${id}`, updateData);
  },

  // 删除一个角色
  deleteCharacter(id) {
    return apiClient.delete(`/characters/${id}`);
  },
  
  getEnums() {
    return apiClient.get('/utils/enums');
  },
};