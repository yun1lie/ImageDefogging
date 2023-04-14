<template>
  <div class="container">
    <div class="upload-container">
      <el-upload
        class="upload-demo"
        action="/api/uploadImage"
        :before-upload="beforeUpload"
        :on-success="handleSuccess"
      >
        <div class="upload-area">
          <i class="el-icon-upload"></i>
          <div class="tip">点击上传图片</div>
        </div>
      </el-upload>
    </div>

    <div class="image-container" v-show="imageUrl2">
      <el-image :src="imageUrl" fit="contain"></el-image>

      <el-image :src="imageUrl2" fit="contain"></el-image>
    </div>

    <div class="button-container">
      <el-button class="process-btn" type="success" @click="handleImage">
        处理图片
      </el-button>
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
    };
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
      console.log(response);
      this.imageUrl = response.data.imageUrl;
      this.imageUrl2 = response.data.imageUrl;
    },
    async handleImage() {
      try {
        // 获取当前屏幕截图路径
        const screenImageUrl = this.imageUrl;
        // 发送 POST 请求并携带图片路径数据
        const response = await axios.post("/api/handleImage", {
          screenImageUrl,
        });
        console.log(response);
        // 解析响应数据
        if (response.data.result === "success") {
          // 更新图片路径并在页面上显示新图片
          this.imageUrl2 = response.data.url;
          console.log(response.data.url);
        } else {
          this.$message.error("图片处理失败：" + response.data.message);
        }
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
}

.upload-container {
  width: 500px;
  height: 250px;
  border: 2px dashed #ddd;
  display: flex;
  justify-content: center;
  align-items: center;
}

.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #999;
  font-size: 16px;
}

.upload-area i {
  font-size: 50px;
}

.image-container {
  margin-top: 25px;
}

.button-container {
  margin-top: 25px;
}

.process-btn {
  background-color: #4caf50;
  color: #fff;
}

.tip {
  margin-top: 10px;
  text-align: center;
}

.el-image__inner {
  max-height: 500px;
  width: auto !important;
}
</style>
