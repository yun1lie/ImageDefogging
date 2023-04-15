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
          v-model.lazy.trim="loginForm.username"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input
          type="password"
          v-model.lazy.trim="loginForm.password"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-checkbox
          v-model="loginForm.remember"
          label="记住密码"
        ></el-checkbox>
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
    async checkLogin() {
      try {
        const response = await axios.post("/api/login", {
          username: this.loginForm.username,
          password: this.loginForm.password,
        });

        // 判断服务器返回的数据中是否有 token
        if (response.data.token) {
          // 说明登录成功
          // 将服务器返回的 token 保存在本地，供后续使用
          localStorage.setItem("token", response.data.token);

          return true;
        } else {
          // 说明登录失败
          // 显示后端返回的错误消息
          this.error = response.data.error;
          return false;
        }
      } catch (error) {
        // 登录失败后的处理
        console.error(error);
        // 显示错误提示信息
        this.error = "登录失败，请检查用户名和密码！";
        return false;
      }
    },

    async login() {
      try {
        if (await this.checkLogin()) {
          // 执行登录逻辑
          console.log("登录成功！");
          // 进行页面跳转等其他操作
          this.$router.push("/userHome");
        } else {
          // 显示表单错误信息
          this.showError = true;
        }
      } catch (error) {
        console.error(error);
      }
    },

    forgotPassword() {
      // 执行忘记密码逻辑
      alert("请联系客服找回密码");
    },

    resetForm() {
      Object.assign(this.loginForm, {
        username: "",
        password: "",
        remember: false,
      });
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
