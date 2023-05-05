<template>
  <div>
    <!-- 头部区域 -->
    <Header />
    <el-form :model="form" ref="form" :rules="rules" label-position="top">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="form.username"></el-input>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="form.email"></el-input>
      </el-form-item>
      <el-form-item label="电话" prop="phone">
        <el-input v-model="form.phone"></el-input>
      </el-form-item>
      <el-form-item label="真实姓名" prop="real_name">
        <el-input v-model="form.real_name"></el-input>
      </el-form-item>
      <el-form-item label="部门" prop="department">
        <el-input v-model="form.department"></el-input>
      </el-form-item>
      <el-form-item label="角色" prop="role">
        <el-input v-model="form.role"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm">提交</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
    <!-- 底部区域 -->
    <Footer />
  </div>
</template>

<script>
import axios from "axios";
import Header from "./Header";
import Footer from "./Footer";
export default {
  components: {
    Header,
    Footer,
  },
  computed: {
    user() {
      return this.token ? JSON.parse(localStorage.getItem("user")).user : null;
    },
    // form() {
    //   return this.token ? JSON.parse(localStorage.getItem("user")).user : null;
    // },
    token() {
      return localStorage.getItem("token");
    },
  },
  created() {
    console.log(this.user);

    this.form.department = this.user.department;
    this.form.username = this.user.username;
    this.form.email = this.user.email;
    this.form.phone = this.user.phone;
    this.form.real_name = this.user.real_name;
    this.form.role = this.user.role;
    this.form.id = this.user.id;
  },
  data() {
    return {
      form: {
        id: "",
        username: "",
        email: "",
        phone: "",
        real_name: "",
        department: "",
        role: "",
      },
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
        ],
        email: [{ required: true, message: "请输入邮箱", trigger: "blur" }],
        phone: [{ required: true, message: "请输入电话号码", trigger: "blur" }],
        real_name: [
          { required: true, message: "请输入真实姓名", trigger: "blur" },
        ],
        department: [
          { required: true, message: "请输入部门", trigger: "blur" },
        ],
        role: [{ required: true, message: "请输入角色", trigger: "blur" }],
      },
    };
  },
  methods: {
    submitForm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          // 提交表单数据到后端接口
          console.log(this.form);
          // 发送请求
          axios
            .post("/api/userMan", this.form)
            .then((res) => {
              console.log("aaa", res);
              if (res.status === 200) {
                // 修改成功，跳转到查看用户信息页面
                alert("修改成功");
                location.reload();
                // this.$router.push("/UserInfo");
              } else {
              }
            })
            .catch((err) => {
              console.log(err);
            });
        } else {
          console.log("表单验证失败");
          return false;
        }
      });
    },
    resetForm() {
      this.$refs.form.resetFields();
    },
  },
};
</script>
