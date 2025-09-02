import { createRouter, createWebHistory } from 'vue-router';
import DashboardView from '../views/DashboardView.vue';

// 定义路由规则
const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: DashboardView,
  },
  {
    path: '/characters',
    name: 'CharacterList',
    // 使用路由懒加载 (Route Lazy Loading)
    // 这意味着 CharacterListView 组件只会在用户访问 /characters 路径时才会被加载
    // 这对于优化应用的初始加载速度非常有帮助
    component: () => import('../views/CharacterListView.vue'),
  },
  // 未来我们可以在这里添加角色详情页的路由
  // {
  //   path: '/characters/:id',
  //   name: 'CharacterDetail',
  //   component: () => import('../views/CharacterDetailView.vue'),
  // }
];

// 创建路由实例
const router = createRouter({
  // 使用 HTML5 History 模式，URL 看起来会更“正常”（没有 #）
  history: createWebHistory(),
  routes, // routes: routes 的简写
});

export default router;