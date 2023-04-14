<template>
  <el-form
    :model="loginForm"
    ref="loginForm"
    :rules="loginRules"
    label-width="80px"
    v-on:submit.prevent="login"
  >
    <el-form-item label="用户名" prop="username">
      <el-input v-model="loginForm.username" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="password">
      <el-input
        type="password"
        v-model="loginForm.password"
        autocomplete="off"
      ></el-input>
    </el-form-item>
    <el-form-item>
      <el-checkbox v-model="loginForm.remember" label="记住密码"></el-checkbox>
      <el-link v-on:click="forgotPassword">忘记密码？</el-link>
    </el-form-item>
    <el-form-item>
      <el-button type="text" v-on:click="resetForm">重置</el-button>
      <el-button type="primary" native-type="submit" @click="login"
        >登录</el-button
      >
    </el-form-item>
    <el-form-item v-if="showError" class="error-message">
      <span>{{ error }}</span>
    </el-form-item>
  </el-form>
</template>

<script>
import axios from "axios";
export default {
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
    checkLogin() {
      // 向服务器发起 POST 请求，发送登录表单数据
      axios
        .post("/api/login", {
          username: this.loginForm.username,
          password: this.loginForm.password,
        })
        .then((response) => {
          // 登录成功后的处理
          console.log("登录成功！");
          console.log(response);

          // 判断服务器返回的数据中是否有 token
          if (response.data.token) {
            // 说明登录成功
            // 将服务器返回的 token 保存在本地，供后续使用
            localStorage.setItem("token", response.data.token);

            // 进行页面跳转等其他操作
            this.$router.push("/userHome");

            return true;
          } else {
            // 说明登录失败
            // 显示后端返回的错误消息
            alert(response.data.error);
            return false;
          }
        })
        .catch((error) => {
          // 登录失败后的处理
          console.error(error);
          // 显示错误提示信息
          alert("登录失败，请检查用户名和密码！");
          return false;
        });
    },

    login() {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          if (this.checkLogin()) {
            // 执行登录逻辑
          } else {
            // 显示表单错误信息
            this.showError = true;
          }
        } else {
          return false;
        }
      });
    },
    forgotPassword() {
      // 执行忘记密码逻辑
    },
    resetForm() {
      Object.assign(this.loginForm, {
        username: "",
        password: "",
        remember: false,
      });
    },
  },
};
</script>

<style scoped>
.error-message span {
  color: red;
}
</style>