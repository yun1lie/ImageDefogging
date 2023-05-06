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
    };
  },
  mounted() {
    // 将echarts实例绑定到Vue实例的$echarts属性上
    this.myEcharts();
  },
  methods: {
    myEcharts() {
      var myChart = this.$echarts.init(document.getElementById("main"));
      //配置图表
      var option = {
        title: {
          text: "echarts入门示例",
        },
        tooltip: {},
        legend: {
          data: ["销量"],
        },
        xAxis: {
          data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
        },
        yAxis: {},
        series: [
          {
            name: "销量",
            type: "bar",
            data: [5, 20, 36, 10, 10, 20],
          },
        ],
      };
      myChart.setOption(option);
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