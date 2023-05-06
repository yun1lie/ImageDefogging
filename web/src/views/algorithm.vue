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
      <div id="main" style="width: 600px; height: 400px"></div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import VueECharts from "vue-echarts";
import echarts from "echarts";

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
      var myChart = this.$echarts.init(document.getElementById("main"));
      // 配置图表
      var option = {
        title: {
          text: "算法使用情况统计",
        },
        tooltip: {},
        legend: {
          data: ["retinex算法", "DCP算法"],
        },
        xAxis: {
          type: "category",
          data: ["retinex算法", "DCP算法"],
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            name: "使用次数",
            type: "bar",
            data: [this.retinexCount, this.dcpCount],
          },
        ],
      };
      myChart.setOption(option);
    },
    async getAlgorithmUsage() {
      try {
        const response = await fetch("/api/algorithm-usage");
        const data = await response.json();

        axios
          .get("/api/algorithm-usage")
          .then((response) => {
            console.log(response.data);
            this.retinexCount = data.retinexCount;
            this.dcpCount = data.dcpCount;
          })
          .catch((error) => {
            console.error(error);
          });

        // 更新图表数据
        this.updateChartData();
      } catch (error) {
        console.error(error);
      }
    },
    updateChartData() {
      // 获取图表实例
      const myChart = echarts.getInstanceByDom(document.getElementById("main"));
      // 更新图表数据
      myChart.setOption({
        series: [
          {
            data: [this.retinexCount, this.dcpCount],
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