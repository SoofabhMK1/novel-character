<template>
  <div class="common-layout">
    <el-header class="app-header">
      <div class="header-content">
        <!-- Logo / Title -->
        <div class="logo-area">
          <h2 class="logo-title">角色管理面板</h2>
        </div>

        <!-- Navigation Menu -->
        <!-- el-menu 不再被一个额外的 div 包裹 -->
        <el-menu
          :default-active="activeIndex"
          mode="horizontal"
          :router="true"
          background-color="transparent"
          text-color="#ffffffb3"
          active-text-color="#ffffff"
          class="header-menu"
        >
          <el-menu-item index="/">仪表盘</el-menu-item>
          <el-menu-item index="/characters">角色列表</el-menu-item>
        </el-menu>
      </div>
    </el-header>

    <el-main class="app-main">
      <div class="main-content-wrapper">
        <router-view />
      </div>
    </el-main>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const activeIndex = computed(() => {
  // 让 "角色列表" 相关的页面也能高亮 "角色列表" 菜单
  if (route.path.startsWith('/characters')) {
    return '/characters';
  }
  return route.path;
});
</script>

<style scoped>
.common-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background-color: #2c3e50;
  color: white;
  padding: 0 20px;
}

.header-content {
  max-width: 1200px;
  height: 100%;
  margin: 0 auto;
  display: flex;
  align-items: center; /* 垂直居中 */
}

.logo-area {
  margin-right: 40px; /* Logo 和菜单之间的固定间距 */
}

.logo-title {
  margin: 0;
  font-weight: 500;
  white-space: nowrap; /* 防止标题换行 */
}

.header-menu {
  border-bottom: none;
  /* 关键：让菜单填满剩余空间 */
  flex-grow: 1; 
}

/* 增强激活状态的视觉效果 */
.header-menu .el-menu-item.is-active {
  border-bottom: 2px solid #409eff !important;
  background-color: rgba(255, 255, 255, 0.1) !important;
}

.app-main {
  flex-grow: 1;
  background-color: #f4f7f6;
  padding: 0; /* 移除 main 的 padding */
  overflow-y: auto;
}

.main-content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px; /* 将 padding 应用到 wrapper 上 */
}
</style>