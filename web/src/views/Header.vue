<template>
  <el-header height="80px">
    <div class="logo">Logo</div>
    <div class="nav">
      <el-menu :default-active="$route.path" mode="horizontal">
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/about">关于我们</el-menu-item>
        <el-menu-item index="/contact">联系我们</el-menu-item>
      </el-menu>
    </div>
    <div class="user-info">
      <el-dropdown>
        <span class="el-dropdown-link">
          <i class="el-icon-user"></i> 用户名<i
            class="el-icon-arrow-down el-icon--right"
          ></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item>个人信息</el-dropdown-item>
          <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </el-header>
</template>

<script>
export default {
  methods: {
    handleLogout() {
      // 执行退出登录逻辑
    },
  },
};
</script>