<template>
  <div>
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
    >
      <el-menu-item index="1">管理用户</el-menu-item>
      <el-menu-item index="2">查询算法使用统计</el-menu-item>
    </el-menu>

    <div id="main" style="width: 600px; height: 400px"></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      algorithmUsage: [
        { algorithm: "Retinex", usageCount: 0 },
        { algorithm: "DCP", usageCount: 0 },
      ],
    };
  },
  computed: {
    chartData() {
      const labels = this.algorithmUsage.map((item) => item.algorithm);
      const data = this.algorithmUsage.map((item) => item.usageCount);
      return {
        labels,
        datasets: [
          {
            label: "算法使用次数",
            backgroundColor: "#409EFF",
            data,
          },
        ],
      };
    },
  },
  methods: {
    handleSelect(index) {
      this.activeIndex = index;
      if (index === "1") {
        this.$router.push("/adminHome");
      } else if (index === "2") {
        this.$router.push("/algorithm");
      }
    },
  },
};
</script>

<style>
</style>