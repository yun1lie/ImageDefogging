根据提供的表结构，修改后的用户注册表单代码如下：

<template>
  <div class="register-wrapper">
    <el-form
      ref="form"
      :model="form"
      label-width="100px"
      class="register-form"
      @submit.native.prevent="submitForm"
    >
      <h2 class="register-title">用户注册</h2>
      <el-form-item
        label="用户名"
        prop="username"
        :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]"
      >
        <el-input
          v-model="form.username"
          autocomplete="off"
          placeholder="请输入4-16位用户名"
          class="register-input"
        ></el-input>
        <span slot="append">
          <i class="el-icon-info"></i> 4-16个字符，支持中英文、数字、下划线
        </span>
      </el-form-item>

      <!-- 密码 -->
      <el-form-item
        label="密码"
        prop="password"
        :rules="[{ required: true, message: '请输入密码', trigger: 'blur' }]"
      >
        <el-input
          type="password"
          v-model="form.password"
          autocomplete="off"
          placeholder="请输入6-16位密码"
          class="register-input"
        ></el-input>
        <span slot="append">
          <i class="el-icon-info"></i>
          6-16个字符，支持中英文、数字、符号，区分大小写
        </span>
      </el-form-item>

      <!-- 确认密码 -->
      <el-form-item
        label="确认密码"
        prop="confirmPassword"
        :rules="[
          { required: true, message: '请再次输入密码', trigger: 'blur' },
          { validator: validateConfirmPassword, trigger: 'blur' },
        ]"
      >
        <el-input
          type="password"
          v-model="form.confirmPassword"
          autocomplete="off"
          placeholder="请再次输入密码"
          class="register-input"
        ></el-input>
        <span slot="append"> <i class="el-icon-info"></i> 请再次输入密码 </span>
      </el-form-item>

      <!-- 邮箱 -->
      <el-form-item
        label="邮箱"
        prop="email"
        :rules="[
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' },
        ]"
      >
        <el-input
          v-model="form.email"
          autocomplete="off"
          placeholder="请输入邮箱地址"
          class="register-input"
        ></el-input>
        <span slot="append">
          <i class="el-icon-info"></i> 请输入有效的邮箱地址
        </span>
      </el-form-item>

      <!-- 电话 -->
      <el-form-item
        label="电话"
        prop="phone"
        :rules="[
          { required: true, message: '请输入电话号码', trigger: 'blur' },
          {
            pattern: /^1[34578]\d{9}$/,
            message: '请输入正确的电话格式',
            trigger: 'blur',
          },
        ]"
      >
        <el-input
          v-model="form.phone"
          autocomplete="off"
          placeholder="请输入电话号码"
          class="register-input"
        ></el-input>
        <span slot="append">
          <i class="el-icon-info"></i> 请输入有效的电话号码
        </span>
      </el-form-item>

      <!-- 真实姓名 -->
      <el-form-item
        label="真实姓名"
        prop="realName"
        :rules="[
          { required: true, message: '请输入真实姓名', trigger: 'blur' },
        ]"
      >
        <el-input
          v-model="form.realName"
          autocomplete="off"
          placeholder="请输入真实姓名"
          class="register-input"
        ></el-input>
        <span slot="append"> <i class="el-icon-info"></i> 请输入真实姓名 </span>
      </el-form-item>

      <!-- 所属部门 -->
      <el-form-item
        label="所属部门"
        prop="department"
        :rules="[
          { required: true, message: '请输入所属部门', trigger: 'blur' },
        ]"
      >
        <el-input
          v-model="form.department"
          autocomplete="off"
          placeholder="请输入所属部门"
          class="register-input"
        ></el-input>
        <span slot="append"> <i class="el-icon-info"></i> 请输入所属部门 </span>
      </el-form-item>

      <!-- 角色 -->
      <el-form-item
        label="角色"
        prop="role"
        :rules="[{ required: true, message: '请输入角色', trigger: 'blur' }]"
      >
        <el-input
          v-model="form.role"
          autocomplete="off"
          placeholder="请输入角色"
          class="register-input"
        ></el-input>
        <span slot="append"> <i class="el-icon-info"></i> 请输入角色 </span>
      </el-form-item>

      <!-- 用户协议和隐私政策 -->
      <el-form-item class="register-agreement">
        <el-checkbox v-model="form.agreement"></el-checkbox>
        <span>我已阅读并同意</span>
        <el-link type="primary" href="#">用户协议</el-link>
        <span>和</span>
        <el-link type="primary" href="#">隐私政策</el-link>
      </el-form-item>

      <!-- 操作按钮 -->
      <el-form-item>
        <el-button
          type="primary"
          native-type="submit"
          class="register-btn"
          :class="{ 'is-hover': !form.agreement }"
          :disabled="!form.agreement"
        >
          立即注册
        </el-button>
        <el-button @click="resetForm" native-type="reset" class="register-btn">
          重置
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "FogRemovalSystemRegister",
  data() {
    return {
      form: {
        username: "",
        password: "",
        confirmPassword: "",
        email: "",
        phone: "",
        realName: "",
        department: "",
        role: "",
        agreement: false,
      },
      codeUrl: "",
    };
  },
  mounted() {
    // this.getCode();
  },
  methods: {
    // 提交表单
    submitForm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          const params = {
            username: this.form.username,
            password: this.form.password,
            email: this.form.email,
            phone: this.form.phone,
            real_name: this.form.realName,
            department: this.form.department,
            role: this.form.role,
          };
          // 发送请求
          axios
            .post("/api/register", params)
            .then((res) => {
              console.log(res);
              if (res.status === 201) {
                // 注册成功，跳转到登录页面
                this.$router.push("/login");
              } else {
              }
            })
            .catch((err) => {
              console.log(err);
            });
        } else {
          return false;
        }
      });
    },
    // 重置表单
    resetForm() {
      this.$refs.form.resetFields();
    },
    // 校验密码是否一致
    validateConfirmPassword(rule, value, callback) {
      if (value !== this.form.password) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    },
  },
};
</script>

<style scoped>
.register-wrapper {
  /* background-image: url(~assets/images/register-background.jpg); */
  background-size: cover;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-title {
  font-size: 3rem;
  margin-top: 2rem;
  margin-bottom: 4rem;
  text-align: center;
  color: #666;
}

.register-form {
  max-width: 500px;
  width: 100%;
  padding: 3rem 5rem;
  border-radius: 5px;
  background-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.register-input {
  width: 100%;
  border-radius: 5px;
  margin-bottom: 1.5rem;
}

.code-img {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
}

.register-code {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.register-agreement {
  margin-bottom: 2rem;
  font-size: 1.4rem;
  color: #666;
}

.register-btn {
  width: 150px;
  height: 50px;
  border-radius: 30px;
  margin-right: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease-in-out;
}

.register-btn.is-hover:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
}

.register-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>