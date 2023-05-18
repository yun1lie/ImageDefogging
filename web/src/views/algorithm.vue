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

    <div class="Echarts">
      <div id="main" style="width: 900px; height: 400px"></div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import VueECharts from "vue-echarts";
import echarts from "echarts";
const chartOption = {
  title: {
    text: "算法使用情况统计",
  },
  tooltip: {},
  legend: {
    data: ["retinex算法", "DCP算法", "NonLocal算法" , "CLAHE算法", "CAP算法"],
  },
  xAxis: {
    type: "category",
    data: ["retinex算法", "DCP算法", "NonLocal算法" , "CLAHE算法", "CAP算法"],
  },
  yAxis: {
    type: "value",
  },
  series: [
    {
      name: "使用次数",
      type: "bar",
      data: [0, 0, 0, 0, 0],
    },
  ],
};

export default {
  name: "EchartsDemo",
  components: {
    VueECharts,
  },
  data() {
    return {
      activeIndex: "2",
      retinexCount: 0,
      dcpCount: 0,
      NonLocalCount: 0,
      CLAHECount: 0,
      CAPCount: 0,
      myChart: null,
    };
  },
  mounted() {
    // 将echarts实例绑定到Vue实例的$echarts属性上
    this.myEcharts();
    // 获取retinex算法和DCP算法的使用情况
    this.getAlgorithmUsage();
  },
  methods: {
   myEcharts() {
      // 初始化图表实例
      this.myChart = this.$echarts.init(document.getElementById("main"));
      // 绑定图表配置
      this.myChart.setOption(chartOption);
    },
    async getAlgorithmUsage() {
       try {
        const response = await axios.get("/api/algorithm-usage");
        const data = response.data;
        console.log(data.NonLocalCount);
        this.retinexCount = data.retinexCount;
        this.dcpCount = data.dcpCount;
        this.NonLocalCount = data.NonLocalCount;
        this.CLAHECount = data.CLAHECount;
        this.CAPCount = data.capCount;
        // 更新图表数据
        this.updateChartData();
      } catch (error) {
        console.error(error);
      }
    },
    updateChartData() {
      // 获取图表实例
      const myChart = this.$echarts.getInstanceByDom(document.getElementById("main"));
      // 更新图表数据
      myChart.setOption({
        series: [
          {
            data: [this.retinexCount, this.dcpCount, this.NonLocalCount, this.CLAHECount, this.CAPCount],
          },
        ],
      });
    },
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