<script setup lang="ts">
import { Delete, UploadFilled } from '@element-plus/icons-vue'
import useInputconfigStore from '@renderer/store/InputStore'
import { storeToRefs } from 'pinia'

const InputConfigStore = useInputconfigStore()
const {
  fileList,
} = storeToRefs(InputConfigStore)

function openFile() {
  const input = document.getElementById('open') as HTMLInputElement | null
  if (input) {
    input.click()
  }
}

function handleFileChange(event) {
  const files = event.target.files
  if (files.length > 0) {
    handleFiles(files)
  }
}

function handleDrop(event) {
  event.preventDefault()
  const files = event.dataTransfer.files
  if (files.length > 0) {
    handleFiles(files)
  }
}

function handleFiles(files) {
  for (let i = 0; i < files.length; i++) {
    fileList.value.push(files[i])
  }
}

function removeFile(index) {
  fileList.value.splice(index, 1) // 根据索引删除文件
}

function clearFileList() {
  fileList.value = []
}
</script>

<template>
  <div class="flex-container">
    <div>
      <el-button type="primary" :icon="Delete" @click="clearFileList">
        清空
      </el-button>
    </div>
    <div id="wrapper" align="center">
      <div
        class="upload-dragger"
        @dragover.prevent
        @drop="handleDrop"
        @click="openFile()"
      >
        <el-icon class="el-icon--upload" :style="{ fontSize: '50px' }">
          <UploadFilled />
        </el-icon>
        <div class="el-upload__text">
          将文件拖到此处，或<em>点击上传</em>
        </div>
      </div>

      <div align="center">
        <ul class="el-upload-list el-upload-list--text">
          <li v-for="(file, index) in fileList" :key="index" class="el-upload-list__item is-success" tabindex="0">
            <div class="el-upload-list__item-info">
              <a class="el-upload-list__item-name">
                <i class="el-icon el-icon--document">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                    <path fill="currentColor" d="M832 384H576V128H192v768h640zm-26.496-64L640 154.496V320zM160 64h480l256 256v608a32 32 0 0 1-32 32H160a32 32 0 0 1-32-32V96a32 32 0 0 1 32-32m160 448h384v64H320zm0-192h160v64H320zm0 384h384v64H320z" />
                  </svg>
                </i>
                <span class="el-upload-list__item-file-name" :title="file.path">{{ file.path }}</span>
              </a>
            </div>
            <label class="el-upload-list__item-status-label">
              <i class="el-icon el-icon--upload-success el-icon--circle-check">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                  <path fill="currentColor" d="M512 896a384 384 0 1 0 0-768 384 384 0 0 0 0 768m0 64a448 448 0 1 1 0-896 448 448 0 0 1 0 896" />
                  <path fill="currentColor" d="M745.344 361.344a32 32 0 0 1 45.312 45.312l-288 288a32 32 0 0 1-45.312 0l-160-160a32 32 0 1 1 45.312-45.312L480 626.752l265.344-265.408z" />
                </svg>
              </i>
            </label>
            <i class="el-icon el-icon--close" @click="removeFile(index)">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                <path fill="currentColor" d="M764.288 214.592 512 466.88 259.712 214.592a31.936 31.936 0 0 0-45.12 45.12L466.752 512 214.528 764.224a31.936 31.936 0 1 0 45.12 45.184L512 557.184l252.288 252.288a31.936 31.936 0 0 0 45.12-45.12L557.12 512.064l252.288-252.352a31.936 31.936 0 1 0-45.12-45.184z" />
              </svg>
            </i>
            <i class="el-icon--close-tip">press delete to remove</i>
          </li>
        </ul>
      </div>

      <div align="center">
        <input id="open" type="file" name="filename" style="display:none" multiple @change="handleFileChange">
      </div>
    </div>
  </div>
</template>

<style scoped>
.upload-dragger {
  border: 2px dashed #e2e2e2;
  border-radius: 6px;
  padding: 20px;
  height: 100px;
  cursor: pointer;
  transition: border-color 0.3s ease;
}
.upload-dragger:hover {
  border-color: #409eff;
}

.file-info {
  margin-top: 10px;
}

.file-link {
  display: inline-block;
  color: #333;
  text-decoration: none;
}

.file-link:hover {
  color: #409eff;
}

.file-name {
  margin-left: 5px;
}

.flex-container {
    display: flex;
    flex-direction: column; /* 设置为垂直排列 */
    gap: 15px; /* 可选项，用于设置组件之间的间隔 */
  }
</style>
