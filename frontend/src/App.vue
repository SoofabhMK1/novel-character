<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <div class="header-content">
        <h2 class="logo">角色管理面板</h2>
        <el-menu
          :default-active="activeIndex"
          mode="horizontal"
          :router="true"
          background-color="#3c414a"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="/">仪表盘</el-menu-item>
          <el-menu-item index="/characters">角色列表</el-menu-item>
        </el-menu>
      </div>
    </el-header>
    <el-main>
      <div class="main-content">
        <!-- 路由匹配到的组件将在这里渲染 -->
        <router-view />
      </div>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
// 计算属性，让导航菜单能根据当前 URL 自动高亮
const activeIndex = computed(() => route.path);
</script>

<style scoped>
.app-container {
  height: 100vh;
}
.app-header {
  background-color: #3c414a;
  color: white;
  padding: 0 20px;
}
.header-content {
  display: flex;
  align-items: center;
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
}
.logo {
  margin: 0;
  margin-right: 40px;
}
.el-menu {
  border-bottom: none;
}
.el-main {
  background-color: #eef0f3;
}
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 20px;
}
</style>