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
        <el-form
          class="subscribe-form"
          :model="form"
          :rules="rules"
          ref="form"
          label-width="100px"
        >
          <h2>预约试用</h2>
          <el-form-item label="姓名" prop="name">
            <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="联系方式" prop="phone">
            <el-input v-model="form.phone"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click.prevent="handleSubmit"
              >提交</el-button
            >
          </el-form-item>
        </el-form>
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
      form: {
        name: "",
        phone: "",
      },
      rules: {
        name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
        phone: [
          { required: true, message: "请输入联系方式", trigger: "blur" },
          {
            pattern: /^1\d{10}$/,
            message: "请输入正确的手机号码",
            trigger: "blur",
          },
        ],
      },
    };
  },

  methods: {
    handleSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          axios
            .post("/api/subscribe", this.form)
            .then((response) => {
              this.$message.success("预约成功！");
              // 清空表单
              this.form.name = "";
              this.form.phone = "";
            })
            .catch((error) => {
              console.error(error);
            });
        }
      });
    },
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

.subscribe-form {
  margin-top: 50px;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.subscribe-form h2 {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: left;
}
</style>
