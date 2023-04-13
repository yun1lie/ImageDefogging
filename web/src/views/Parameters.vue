<template>
  <div class="parameters">
    <el-form label-width="100px">
      <el-form-item
        v-for="(item, index) in items"
        :key="index"
        :label="item.label"
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