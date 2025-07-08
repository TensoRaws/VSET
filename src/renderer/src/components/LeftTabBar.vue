<script setup lang="ts">
    import { ref } from 'vue'
    import {
    VideoCameraFilled,
    KnifeFork,
    DishDot,
    List,
    Printer,
    } from '@element-plus/icons-vue'

    const isCollapse = ref(true)


import { useRouter } from "vue-router";

const router = useRouter();

</script>

<template>
   <el-radio-group v-model="isCollapse"  style="margin-bottom: 0px;margin-top: 0px">
    <el-radio-button :value="false">详细</el-radio-button>
    <el-radio-button :value="true">图标</el-radio-button>
  </el-radio-group>

  <el-menu
    default-active="1"
    class="el-menu-vertical-demo"
    :collapse="isCollapse"
    background-color="#DCDCDC"
    :router="true"
  >

    <el-menu-item index="1" @click="router.push('/input')">
      <el-icon><List /></el-icon>
      <template #title>输入设置</template>
    </el-menu-item>


    <el-sub-menu index="2">
          <template #title>
            <el-icon><KnifeFork /></el-icon>
            <span>AI渲染
            </span>
          </template>
            <el-menu-item index="1-1">超分辨率</el-menu-item>
            <el-menu-item index="1-2" disabled>补帧(画饼中)</el-menu-item>
            <el-menu-item index="1-3" disabled>降噪(画饼中)</el-menu-item>
        </el-sub-menu>
    
    <el-menu-item index="3">
      <el-icon><VideoCameraFilled /></el-icon>
      <template #title>滤镜设置</template>
    </el-menu-item>

    <el-menu-item index="4" @click="router.push('/output')">
      <el-icon><DishDot /></el-icon>
      <template #title>输出设置</template>
    </el-menu-item>

    <el-menu-item index="5">
      <el-icon><Printer /></el-icon>
      <template #title>交付</template>
    </el-menu-item>


  </el-menu>


</template>

<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 160px;
  min-height: 400px;
}
</style>