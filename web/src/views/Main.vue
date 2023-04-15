<template>
  <el-main>
    <div class="main-container">
      <div class="header">
        <h1>腹腔镜图像去雾系统</h1>
      </div>
      <Preview />
      <!-- <Parameters /> -->
    </div>
  </el-main>
</template>

<script>
import Parameters from "./Parameters";
import Upload from "./Upload";
import Preview from "./Preview";

export default {
  components: {
    Parameters,
    Preview,
  },

  data() {
    return {
      params: {
        exposure: 1.0,
        contrast: 1.0,
        gamma: 1.0,
      },
      selectedImage: null,
      previewScale: 1.0,
    };
  },

  methods: {
    onFileSelected(file) {
      this.selectedImage = file;
    },

    onScaleChanged(scale) {
      this.previewScale = scale;
    },
  },
};
</script>

<style scoped>
.header {
  background-color: #409eff;
  color: white;
  text-align: center;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.header h1 {
  margin: 0;
  font-size: 32px;
}

.main-container {
  max-width: 800px;
  margin: 30px auto;
  padding: 20px;
  background-color: #f0f2f5;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

/* 其他样式... */
</style>