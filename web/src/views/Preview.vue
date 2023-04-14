<template>
  <div>
    <div class="upload">
      <el-upload
        class="upload-demo"
        action="/api/uploadImage"
        :on-success="handleSuccess"
      >
        <el-button type="primary" icon="el-icon-upload">点击上传图片</el-button>
      </el-upload>
    </div>
    <el-image v-if="imageUrl" :src="imageUrl" fit="contain"></el-image>
    <el-button type="success" icon="el-icon-picture" @click="handleImage"
      >处理图片</el-button
    >
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      imageUrl: "",
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
          this.imageUrl = response.data.url;
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