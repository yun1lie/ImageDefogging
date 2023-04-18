<template>
  <div class="user-info">
    <el-card>
      <div slot="header" class="card-header">
        <h3>{{ userInfo.realName }}</h3>
        <span>{{ userInfo.department }}</span>
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
  </div>
</template>

<script>
export default {
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
  methods: {},
};
</script>

<style scoped>
.user-info {
  max-width: 600px;
  margin: 0 auto;
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