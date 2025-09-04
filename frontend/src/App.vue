<template>
  <div class="common-layout">
    <el-header class="app-header">
      <div class="header-content">
        <!-- Logo / Title -->
        <div class="logo-area">
          <router-link to="/" class="logo-link">
            <img src="/images/logo.png" alt="App Logo" class="logo-image" />
            <h2 class="logo-title">角色管理面板</h2>
          </router-link>
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
          <el-menu-item index="/lore">设定集</el-menu-item>
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
  if (route.path.startsWith('/lore')) {
    return '/lore';
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
  margin-right: 40px;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none; /* 移除链接下划线 */
  color: inherit; /* 继承父元素的文字颜色 */
}

.logo-image {
  height: 40px; /* 关键：控制 Logo 的高度 */
  width: auto; /* 宽度自适应 */
  margin-right: 12px; /* Logo 和文字之间的间距 */
}

.logo-title {
  margin: 0;
  font-weight: 500;
  white-space: nowrap;
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