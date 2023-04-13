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
      <el-button type="primary" native-type="submit">登录</el-button>
    </el-form-item>
    <el-form-item v-if="showError" class="error-message">
      <span>{{ error }}</span>
    </el-form-item>
  </el-form>
</template>

<script>
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
      if (
        this.loginForm.username === "admin" &&
        this.loginForm.password === "123456"
      ) {
        // 执行登录逻辑
        console.log("登录成功！");
        return true;
      } else {
        // 显示表单错误信息
        this.error = "用户名或密码错误";
        return false;
      }
    },
    login() {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          if (this.checkLogin()) {
            // 执行登录逻辑
            console.log("登录成功！");
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