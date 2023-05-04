<template>
  <div class="login-form-container">
    <h1 class="title">腹腔镜图像去雾系统</h1>
    <el-form
      :model="loginForm"
      ref="loginForm"
      :rules="loginRules"
      label-width="80px"
      @submit.native.prevent="login"
    >
      <el-form-item label="用户名" prop="username">
        <el-input
          v-model.trim="loginForm.username"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input
          type="password"
          v-model.trim="loginForm.password"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <!-- <el-checkbox
          v-model="loginForm.remember"
          label="记住密码"
        ></el-checkbox> -->
        <el-link @click="forgotPassword">忘记密码？</el-link>
      </el-form-item>
      <el-form-item>
        <el-button type="text" @click="resetForm">重置</el-button>
        <el-button class="login-button" type="primary" native-type="submit"
          >登录</el-button
        >
      </el-form-item>
      <el-form-item v-if="showError" class="error-message">
        <span>{{ error }}</span>
      </el-form-item>
    </el-form>
    <div class="register-tip">
      还没有账号？立即
      <router-link to="/register">注册</router-link>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginForm",

  data() {
    return {
      loginForm: {
        username: "",
        password: "",
        remember: false,
      },
      loginRules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
      },
      showError: false,
      error: "",
    };
  },

  methods: {
    async checkLoginSuccess(response) {
      // 保存 token
      localStorage.setItem("token", response.data.token);
      this.token = response.data.token;
      console.log("登录成功！");
      return true;
    },

    checkLoginFailure(error) {
      console.error(error);
      this.error = "登录失败，请检查用户名和密码！";
      return false;
    },

    async checkLogin() {
      try {
        const response = await axios.post("/api/login", {
          username: this.loginForm.username,
          password: this.loginForm.password,
        });

        if (response.data.token) {
          return await this.checkLoginSuccess(response);
        } else {
          return this.checkLoginFailure(response.data.error);
        }
      } catch (error) {
        return this.checkLoginFailure(error);
      }
    },

    async login() {
      try {
        if (await this.checkLogin()) {
          axios
            .get("/api/user", {
              headers: { Authorization: `Bearer ${this.token}` },
            })
            .then((response) => {
              localStorage.setItem("user", JSON.stringify(response.data));
              const user = JSON.parse(localStorage.getItem("user"));
              this.realName = user.user.real_name;
              // console.log(this.realName);
              console.log(user.user.role);
              if (user.user.role == "超级管理员") {
                this.$router.push("/adminHome");
              } else {
                this.$router.push("/userHome");
              }
            })
            .catch((error) => {
              console.error(error);
            });

          // this.$router.push("/userHome");
        } else {
          this.showError = true;
        }
      } catch (error) {
        console.error(error);
      }
    },

    forgotPassword() {
      alert("请联系客服找回密码");
    },

    resetForm() {
      this.$refs.loginForm.resetFields();
      this.showError = false;
      this.error = "";
    },
  },
};
</script>

<style scoped>
.login-form-container {
  max-width: 400px;
  margin: 100px auto;
  background-color: #f0f2f5;
  padding: 50px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.title {
  font-size: 32px;
  margin-bottom: 30px;
  text-align: center;
}

.login-button {
  font-size: 20px;
  width: 140px;
}

.error-message span {
  color: red;
}

.register-tip {
  margin-top: 20px;
  text-align: center;
}

.register-tip a {
  color: #409eff;
  text-decoration: underline;
}
</style>