<template>
  <div class="user-info">
    <!-- 头部区域 -->
    <Header />
    <el-card>
      <div slot="header" class="card-header">
        <h3>姓名： {{ userInfo.realName }}</h3>
        <span>所在部门：{{ userInfo.department }}</span>
      </div>
      <div class="card-body">
        <el-row>
          <el-col :span="12" class="form-item">
            <label class="label">用户名：</label>
            <span>{{ userInfo.username }}</span>
          </el-col>
          <el-col :span="12" class="form-item">
            <label class="label">角色：</label>
            <span>{{ userInfo.role }}</span>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12" class="form-item">
            <label class="label">邮箱：</label>
            <span>{{ userInfo.email }}</span>
          </el-col>
          <el-col :span="12" class="form-item">
            <label class="label">电话：</label>
            <span>{{ userInfo.phone }}</span>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12" class="form-item">
            <label class="label">创建时间：</label>
            <span>{{ userInfo.create_time }}</span>
          </el-col>
          <el-col :span="12" class="form-item">
            <label class="label">更新时间：</label>
            <span>{{ userInfo.update_time }}</span>
          </el-col>
        </el-row>
      </div>
    </el-card>

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
  data() {
    return {
      userInfo: {
        username: "",
        update_time: "",
        create_time: "",
        email: "",
        phone: "",
        realName: "",
        department: "",
        role: "",
      },
    };
  },
  methods: {
    // getUserInfo() {
    //   axios
    //     .get("/api/user", {
    //       headers: { Authorization: `Bearer ${this.token}` },
    //     })
    //     .then((response) => {
    //       localStorage.setItem("user", JSON.stringify(response.data));
    //       // console.log(response.data);
    //     })
    //     .catch((error) => {
    //       console.error(error);
    //     });
    // },
  },
  created() {
    this.user = JSON.parse(localStorage.getItem("user")).user;
    console.log(this.user);
    this.userInfo.username = this.user.username;
    console.log(this.userInfo.username);
    this.userInfo.update_time = this.user.update_time;
    this.userInfo.create_time = this.user.create_time;
    this.userInfo.email = this.user.email;
    this.userInfo.phone = this.user.phone;
    this.userInfo.realName = this.user.real_name;
    this.userInfo.department = this.user.department;
    this.userInfo.role = this.user.role;
    // this.getUserInfo();
  },
};
</script>

<style scoped>
.user-info {
  max-width: 1600px;
  margin: 0 auto;
}
.el-header {
  padding: 0 20px;
  box-shadow: 0 1px 3px #ebebeb;
}

.card-header {
  display: flex;
  align-items: center;
  padding: 20px;
}

.card-header h3 {
  margin: 0;
}

.card-header span {
  margin-left: 20px;
  font-size: 14px;
}

.label {
  font-weight: bold;
}

.form-item {
  margin-bottom: 20px;
}

.form-item label {
  width: 100px;
  display: inline-block;
}

.form-item span {
  display: inline-block;
  min-width: 100px;
}

@media (max-width: 768px) {
  .form-item label {
    display: block;
  }
}
</style>