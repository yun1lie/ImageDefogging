<template>
  <div class="container">
    <div class="upload-container">
      <el-upload
        class="upload-demo"
        action="/api/uploadImage"
        :before-upload="beforeUpload"
        :on-success="handleSuccess"
        :show-file-list="false"
      >
        <div class="upload-area" :class="{ disabled: imageUrl === '' }">
          <i class="el-icon-upload"></i>
          <div class="tip">点击上传图片</div>
          <el-image
            class="preview-image"
            :src="imageUrl"
            fit="contain"
          ></el-image>
        </div>

        <div class="success-message" v-if="imageUrl">上传成功！</div>
      </el-upload>
    </div>

    <div class="image-container" v-show="imageUrl2">
      <h2>处理后的图片</h2>
      <!-- <el-image :src="imageUrl" fit="contain"></el-image> -->
      <el-image :src="imageUrl2" fit="contain"></el-image>
    </div>

    <div class="button-container">
      <el-button
        class="process-btn"
        type="success"
        :disabled="imageUrl === '' || isProcessing"
        @click="handleImage"
      >
        <template v-if="!isProcessing"> 处理图片 </template>
        <template v-else>
          <i class="el-icon-loading"></i>
          处理中...
        </template>
      </el-button>
      <div class="processing-message" v-if="isProcessing">
        图片正在处理中，请稍等...
      </div>
      <div class="success-message" v-if="imageUrl2">图片处理成功！</div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      imageUrl: "",
      imageUrl2: "",
      isProcessing: false,
    };
  },
  computed: {
    isSuccess() {
      return this.imageUrl2 !== "";
    },
  },
  methods: {
    beforeUpload(file) {
      const isJPG = file.type === "image/jpeg";
      const isPNG = file.type === "image/png";
      const isGIF = file.type === "image/gif";

      if (!isJPG && !isPNG && !isGIF) {
        this.$message.error("只能上传 JPG/PNG/GIF 文件");
        return false;
      }
      return true;
    },
    handleSuccess(response) {
      this.imageUrl = response.data.imageUrl;
      this.imageUrl2 = response.data.imageUrl;
    },
    async handleImage() {
      try {
        this.isProcessing = true;
        const screenImageUrl = this.imageUrl;

        const response = await axios.post("/api/handleImage", {
          screenImageUrl,
        });

        if (response.data.result === "success") {
          this.imageUrl2 = response.data.url;
        } else {
          this.$message.error("图片处理失败：" + response.data.message);
        }
      } catch (error) {
        console.error(error);
      } finally {
        this.isProcessing = false;
      }
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
}

h1 {
  margin-bottom: 10px;
  font-size: 24px;
  color: #444;
}

p {
  margin-bottom: 20px;
  font-size: 16px;
  color: #666;
}

.upload-container {
  width: 500px;
  height: 250px;
  border: 2px dashed #ddd;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 30px;
}

.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #999;
  font-size: 16px;
  position: relative;
}

.upload-area.disabled {
  opacity: 0.5;
  pointer-events: none;
}

.tip {
  margin-top: 10px;
  text-align: center;
}

.preview-image {
  margin-top: 20px;
}

.success-message {
  color: #4caf50;
  font-size: 14px;
  margin-top: 10px;
}

.image-container {
  margin-top: 25px;
}

h2 {
  font-size: 20px;
  color: #444;
  margin-bottom: 20px;
}

.button-container {
  margin-top: 25px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.process-btn {
  background-color: #4caf50 !important;
  color: #fff !important;
  margin-bottom: 20px;
  min-width: 150px;
}

.process-btn .el-icon-loading {
  margin-right: 10px;
}

.processing-message {
  color: #666;
  font-size: 14px;
  margin-top: 10px;
}

.success-message {
  color: #4caf50;
  font-size: 14px;
  margin-top: 10px;
}
</style>