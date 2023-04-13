<template>
  <div class="home">
    <el-row>
      <el-col
        :xs="{ span: 24 }"
        :sm="{ span: 24 }"
        :md="{ span: 12 }"
        :lg="{ span: 8 }"
      >
        <img src="@/assets/images/logo.jpeg" alt="logo" />
        <h1>腹腔镜图像去雾系统</h1>
        <p>欢迎使用我们的系统，通过去除手术内部雾气，使医生更好地进行手术。</p>
        <router-link to="/login">
          <el-button type="primary" size="medium">登录</el-button>
        </router-link>
      </el-col>
      <el-col
        :xs="{ span: 24 }"
        :sm="{ span: 24 }"
        :md="{ span: 12 }"
        :lg="{ span: 16 }"
      >
        <img src="@/assets/images/home-image.jpeg" alt="home image" />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Home",

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
  max-width: 80px;
  margin-bottom: 20px;
}

.title {
  font-size: 36px;
  margin-top: 30px;
  margin-bottom: 20px;
  font-weight: bold;
}

.comment {
  font-size: 18px;
  margin-bottom: 30px;
}

.login-button {
  font-size: 18px;
  width: 140px;
}

.home-img {
  max-height: 500px;
  object-fit: cover;
}
</style>
