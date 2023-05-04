<template>
  <div>
    <!-- 用户列表 -->
    <el-table :data="users" style="width: 100%">
      <el-table-column prop="id" label="ID"></el-table-column>
      <el-table-column prop="username" label="用户名"></el-table-column>
      <el-table-column prop="email" label="邮箱"></el-table-column>
      <el-table-column prop="phone" label="手机号"></el-table-column>
      <el-table-column prop="real_name" label="真实姓名"></el-table-column>
      <el-table-column prop="department" label="所属部门"></el-table-column>
      <el-table-column prop="role" label="角色"></el-table-column>
      <el-table-column prop="create_time" label="创建时间"></el-table-column>
      <el-table-column prop="update_time" label="更新时间"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="editUser(scope.row)"
            >编辑</el-button
          >
          <el-button type="danger" size="small" @click="deleteUser(scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑用户的对话框 -->
    <el-dialog :visible.sync="dialogVisible" title="编辑用户">
      <el-form :model="user" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="user.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="user.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="user.email"></el-input>
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="user.phone"></el-input>
        </el-form-item>
        <el-form-item label="真实姓名">
          <el-input v-model="user.real_name"></el-input>
        </el-form-item>
        <el-form-item label="所属部门">
          <el-input v-model="user.department"></el-input>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="user.role">
            <el-option label="管理员" value="admin"></el-option>
            <el-option label="普通用户" value="user"></el-option>
          </el-select>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveUser">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: [], // 用户数据列表
      dialogVisible: false, // 添加/编辑用户的对话框是否可见
      user: {
        // 当前正在编辑的用户
        id: null,
        username: "",
        password: "",
        email: "",
        phone: "",
        real_name: "",
        department: "",
        role: "",
        create_time: "",
        update_time: "",
      },
    };
  },
  mounted() {
    // 在组件挂载后加载用户数据
    this.loadUsers();
  },
  methods: {
    loadUsers() {
      // 发送 HTTP 请求加载用户数据，并将结果保存到 users 中
      // 省略具体实现
    },
    addUser() {
      // 打开添加用户的对话框
      this.user = {
        id: null,
        username: "",
        password: "",
        email: "",
        phone: "",
        real_name: "",
        department: "",
        role: "",
        create_time: "",
        update_time: "",
      };
      this.dialogVisible = true;
    },
    editUser(user) {
      // 打开编辑用户的对话框，并将用户数据填入表单中
      this.user = Object.assign({}, user);
      this.dialogVisible = true;
    },
    saveUser() {
      // 发送 HTTP 请求保存修改后的用户数据，并重新加载用户列表
      // 省略具体实现
      this.loadUsers();
      this.dialogVisible = false;
    },
    deleteUser(user) {
      // 发送 HTTP 请求删除指定用户，并重新加载用户列表
      // 省略具体实现
      this.loadUsers();
    },
  },
};
</script>
