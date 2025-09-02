<template>
  <main class="main-content">
    <DashboardView />
  </main>
</template>

<script setup>
import DashboardView from './views/DashboardView.vue';
</script>

<style>
/* 这是一个全局样式，可以影响整个应用 */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: #eef0f3;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
}
</style>