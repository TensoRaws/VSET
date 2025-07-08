<script setup lang="ts">
   import {Refresh,MessageBox} from '@element-plus/icons-vue'
</script>

<template>

<div class="flex-container">
    <div class="mb-4">
      <el-button :icon="MessageBox" type="success"  disabled>保存设置</el-button>
      <el-button :icon="Refresh" type="success"  disabled>恢复默认设置</el-button>
  </div>


  </div>

</template>

<style scoped>


.flex-container {
    display: flex;
    flex-direction: column; /* 设置为垂直排列 */
    gap: 15px; /* 可选项，用于设置组件之间的间隔 */
  }

</style>
