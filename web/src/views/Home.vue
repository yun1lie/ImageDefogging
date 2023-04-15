<template>
  <div class="home">
    <el-row>
      <el-col
        :xs="{ span: 24 }"
        :sm="{ span: 24 }"
        :md="{ span: 12 }"
        :lg="{ span: 8 }"
      >
        <img class="logo-img" src="@/assets/images/logo.jpeg" alt="logo" />
        <h1 class="title">腹腔镜图像去雾系统</h1>
        <p class="comment">
          欢迎使用我们的系统，通过去除手术内部雾气，使医生更好地进行手术。
        </p>
        <router-link to="/login">
          <el-button class="login-button" type="primary" size="medium"
            >登录</el-button
          >
        </router-link>
      </el-col>
      <el-col
        :xs="{ span: 24 }"
        :sm="{ span: 24 }"
        :md="{ span: 12 }"
        :lg="{ span: 16 }"
      >
        <img
          class="home-img"
          src="@/assets/images/home-image.jpeg"
          alt="home image"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Home",

  data() {
    return {
      message: "",
    };
  },

  mounted() {
    console.log("bbbbbbbbbb");
    // 在组件挂载后发送请求并更新数据
    axios
      .get("/api/")
      .then((response) => {
        this.message = response.data;
        console.log("aaaaa");
        console.log(this.message);
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>

<style scoped>
.home {
  padding: 50px;
  text-align: center;
}

.logo-img {
  max-width: 150px;
  margin-bottom: 20px;
}

.title {
  font-size: 48px;
  margin-top: 30px;
  margin-bottom: 20px;
  font-weight: bold;
}

.comment {
  font-size: 20px;
  margin-bottom: 30px;
  line-height: 1.5;
}

.login-button {
  font-size: 20px;
  width: 140px;
}

.home-img {
  max-height: 600px;
  object-fit: cover;
}
</style>
