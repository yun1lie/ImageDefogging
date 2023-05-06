<template>
  <div>
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
      <el-menu-item index="1">管理用户</el-menu-item>
      <el-menu-item index="2">查询算法使用统计</el-menu-item>
    </el-menu>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeIndex: '1'
    };
  },
  methods: {
    handleSelect(index) {
      this.activeIndex = index;
      if (index === '1') {
        this.$router.push('/adminHome');
      } else if (index === '2') {
        this.$router.push('/algorithm');
      }
    }
  }
};
</script>

<style>
.el-menu-demo {
  margin-bottom: 10px;
}
</style>
