<template>
  <el-header height="80px">
    <div class="logo"><img src="@/assets/images/logo.jpeg" alt="" /></div>
    <div class="nav">
      <el-menu :default-active="$route.path" mode="horizontal">
        <el-menu-item index="/"
          ><router-link to="/">首页</router-link></el-menu-item
        >
      </el-menu>
    </div>
    <div class="user-info">
      <!-- 如果用户已登录，则展示用户信息和退出登录按钮 -->
      <el-dropdown v-if="user && token">
        <span class="el-dropdown-link">
          <i class="el-icon-user">{{ this.realName }}</i>
          <i class="el-icon-arrow-down el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item @click="handleUserInfo">个人信息</el-dropdown-item>
          <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <!-- 如果用户未登录，则展示登录链接 -->
      <router-link v-else to="/login">登录</router-link>
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
      this.$router.push("/"); // 跳转到首页
    },
    handleUserInfo() {
      this.$message.info(`用户姓名：${this.realName}`);
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

<!-- 样式 -->
<style scoped>
.header {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0 50px;
}

.logo {
  font-size: 32px;
  color: #333;
  margin-right: 20px;
  display: flex;
  align-items: center;
}
.logo img {
  margin-top: 10px;
  height: 50px;
}

.nav {
  display: flex;
  align-items: center;
}

/* .user-info {
  position: absolute;
  right: 30px;
  top: 50%;
  transform: translateY(-50%);
  line-height: 1;
} */
</style>