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
      <!-- 如果用户已登录，则展示用户信息和退出登录按钮 -->
      <el-dropdown v-show="user && token">
        <span class="el-dropdown-link">
          <i class="el-icon-user">{{this.realName}}</i>
          <i class="el-icon-arrow-down el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item>个人信息</el-dropdown-item>
          <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <!-- 如果用户未登录，则展示登录链接 -->
      <router-link v-show="!user || !token" to="/login">登录</router-link>
    </div>
  </el-header>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return { realName: null };
  },
  computed: {
    user() {
      return this.token ? JSON.parse(localStorage.getItem("user")) : null;
    },
    token() {
      return localStorage.getItem("token");
    },
  },
  methods: {
    handleLogout() {
      localStorage.removeItem("token"); // 清空本地存储中的 Token
      localStorage.removeItem("user"); // 清空本地存储中的 User
    },
    getUserInfo() {
      axios
        .get("/api/user", {
          headers: { Authorization: `Bearer ${this.token}` },
        })
        .then((response) => {
          localStorage.setItem("user", JSON.stringify(response.data));
          const user = JSON.parse(localStorage.getItem("user"));
          this.realName = user.user.real_name;
          console.log(this.realName);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  mounted() {
    if (this.token) {
      this.getUserInfo();
    }
  },
};
</script>
