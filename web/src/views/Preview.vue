<template>
  <div class="container">
    <div class="select">
      <el-radio-group v-model="radio1">
        <el-radio-button label="D"></el-radio-button>
        <el-radio-button label="DCP"></el-radio-button>
        <el-radio-button label="广州"></el-radio-button>
        <el-radio-button label="深圳"></el-radio-button>
      </el-radio-group>
    </div>
    <div class="upload-container">
      <el-upload
        class="upload-demo"
        action="/api/uploadImage"
        :before-upload="beforeUpload"
        :on-success="handleSuccess"
        :show-file-list="false"
      >
        <div class="upload-area" :class="{ disabled: imageUrl === '' }">
          <i class="el-icon-upload" v-if="imageUrl == ''"></i>
          <div class="tip" v-if="imageUrl == ''">点击上传图片</div>
          <el-image
            class="preview-image"
            :src="imageUrl"
            fit="contain"
            v-if="imageUrl"
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
      <div class="success-message" v-if="imageUrl2 != imageUrl">
        图片处理成功！
      </div>
    </div>

    <div class="pr" v-if="radio1 === 'DCP'">
      <h1>参数设置</h1>
      <div class="block">
        <span class="demonstration">min_filter_radius</span>
        <el-slider
          class="slider"
          v-model="min_filter_radius"
          :min="1"
          :max="50"
        />
      </div>
      <div class="block">
        <span class="demonstration">引导滤波半径</span>
        <el-slider
          class="slider"
          v-model="guided_filter_radius"
          :min="1"
          :max="100"
        />
      </div>

      <div class="block">
        <span class="demonstration">引导滤波epsilon</span>
        <el-slider
          class="slider"
          v-model="guided_filter_epsilon"
          :min="0"
          :max="0.1"
          :step="0.001"
        />
      </div>

      <div class="block">
        <span class="demonstration">v1限制</span>
        <el-slider
          class="slider"
          v-model="v1_limit"
          :min="0"
          :max="1"
          :step="0.01"
        />
      </div>

      <div class="block">
        <span class="demonstration">v1权重</span>
        <el-slider
          class="slider"
          v-model="v1_weight"
          :min="0"
          :max="1"
          :step="0.01"
        />
      </div>

      <div class="block">
        <span class="demonstration">直方图区间数</span>
        <el-slider class="slider" v-model="bins" :min="1" :max="5000" />
      </div>

      <div class="block">
        <span class="demonstration">伽马校正</span>
        <el-switch
          v-model="gamma_correction_enabled"
          active-text="开启"
          inactive-text="关闭"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      min_filter_radius: 7,
      guided_filter_radius: 81,
      guided_filter_epsilon: 0.001,
      v1_limit: 0.8,
      v1_weight: 0.95,
      bins: 2000,
      gamma_correction_enabled: false,
      imageUrl: "",
      imageUrl2: "",
      isProcessing: false,
      radio1: "D",
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
      console.log("目前算法为:", this.radio1);
      if (this.radio1 == "D") {
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
      }

      if (this.radio1 == "DCP") {
        try {
          this.isProcessing = true;
          const screenImageUrl = this.imageUrl;
          const min_filter_radius = this.min_filter_radius;
          const guided_filter_radius = this.guided_filter_radius;
          const guided_filter_epsilon = this.guided_filter_epsilon;
          const v1_limit = this.v1_limit;
          const v1_weight = this.v1_weight;
          const bins = this.bins;
          const gamma_correction_enabled = this.gamma_correction_enabled;
          const response = await axios.post("/api/handleDCP", {
            screenImageUrl,
            min_filter_radius,
            guided_filter_radius,
            guided_filter_epsilon,
            v1_limit,
            v1_weight,
            bins,
            gamma_correction_enabled,
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
      }
    },
  },
};
</script>

<style scoped>
.pr {
  width: 600px;
}
.block {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  width: 100%;
}

.demonstration {
  flex-basis: 30%;
  font-size: 14px;
  font-weight: bold;
  margin-right: 10px;
}

.slider {
  flex-basis: 60%;
  margin-right: 10px;
}

.el-input-number {
  flex-basis: 20%;
}
.select {
  margin-bottom: 100px;
}
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