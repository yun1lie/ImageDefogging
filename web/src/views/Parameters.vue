<template>
  <div class="parameters">
    <el-form label-position="top" class="form-container">
      <el-form-item
        v-for="(item, index) in items"
        :key="index"
        :label="item.label"
        class="form-item"
      >
        <el-slider v-model="item.value" :min="0" :max="100"></el-slider>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      items: [
        {
          label: "雾的强度",
          value: 50,
        },
        {
          label: "透视度",
          value: 50,
        },
        {
          label: "光照",
          value: 50,
        },
      ],
    };
  },
};
</script>

<style scoped>
.parameters {
  max-width: 800px;
  margin: 30px auto;
}

.form-container {
  display: flex;
  flex-wrap: wrap;
}

.form-item {
  width: calc(100% / 3 - 20px);
  margin-right: 20px;
  margin-bottom: 20px;
}

.el-slider__button-wrapper {
  border: none !important;
}

.el-slider__runway {
  height: 4px;
  background-color: #e4e7ed;
  border-radius: 2px;
}

.el-slider__bar {
  height: 4px;
  background-color: #409eff;
  border-radius: 2px;
}

.el-slider__button {
  width: 14px;
  height: 14px;
  margin-top: -5px;
  margin-left: -7px;
  background-color: #409eff;
  border-color: #409eff;
  box-shadow: none;
}
</style>