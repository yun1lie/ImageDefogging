<template>
  <div>
    <!--用户查询-->
    <el-form :inline="true" :model="searchForm" class="search-form">
      <el-form-item label="用户名">
        <el-input v-model="searchForm.name"></el-input>
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="searchForm.email"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSearch">查询</el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleCreate">添加用户</el-button>
      </el-form-item>
    </el-form>

    <!--用户列表-->
    <el-table :data="userList" style="width: 100%">
      <el-table-column prop="id" label="ID"></el-table-column>
      <el-table-column prop="username" label="用户名"></el-table-column>
      <el-table-column prop="email" label="电子邮箱"></el-table-column>
      <el-table-column prop="phone" label="电话"></el-table-column>
      <el-table-column prop="real_name" label="姓名"></el-table-column>
      <el-table-column prop="department" label="科室"></el-table-column>
      <el-table-column prop="role" label="职位"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button type="text" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button type="text" @click="handleDelete(scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <!--用户编辑-->
    <el-dialog :visible.sync="editDialogVisible" title="编辑用户">
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="editForm.username"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="editForm.email"></el-input>
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="editForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="editForm.real_name"></el-input>
        </el-form-item>
        <el-form-item label="科室">
          <!-- <el-select v-model="value" placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
               v-model="editForm.department"
            >
            </el-option>
          </el-select> -->
          <el-input v-model="editForm.department"></el-input>
        </el-form-item>
        <el-form-item label="职位">
          <!-- <el-select v-model="value" placeholder="请选择"> -->
          <!-- <el-option
              v-for="item in options2"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select> -->
          <el-input v-model="editForm.role"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleEditConfirm">确 定</el-button>
      </div>
    </el-dialog>

    <!--用户添加-->
    <el-dialog :visible.sync="createDialogVisible" title="添加用户">
      <el-form :model="createForm" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="createForm.name"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="createForm.email"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="createForm.password"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="createDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleCreateConfirm">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  created() {
    axios
      .get("/api/users")
      .then((response) => {
        console.log(response.data.users);
        this.userList = response.data.users;
      })
      .catch((error) => {
        console.error(error);
      });
  },

  data() {
    return {
      options: [
        {
          value: "内科",
          label: "内科",
        },
        {
          value: "儿科",
          label: "儿科",
        },
        {
          value: "神经科",
          label: "神经科",
        },
        {
          value: "系统管理部门",
          label: "系统管理部门",
        },
      ],
      options2: [
        {
          value: "医生",
          label: "医生",
        },
        {
          value: "护士",
          label: "护士",
        },
        {
          value: "超级管理员",
          label: "超级管理员",
        },
      ],
      searchForm: {
        name: "",
        email: "",
      },
      userList: [],
      editDialogVisible: false,
      editForm: {
        username: "",
        email: "",
        phone: "",
        real_name: "",
        department: "",
        role: "",
      },
      createDialogVisible: false,
      createForm: {
        name: "",
        email: "",
        password: "",
      },
    };
  },
  methods: {
    handleSearch() {
      axios
        .get("/api/user", {
          params: {
            name: this.searchForm.name,
            email: this.searchForm.email,
          },
        })
        .then((response) => {
          this.userList = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    handleCreate() {
      this.createDialogVisible = true;
    },
    handleCreateConfirm() {
      axios
        .post("/api/user", this.createForm)
        .then((response) => {
          this.userList.push(response.data);
          this.createDialogVisible = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    handleEdit(row) {
      this.editForm = Object.assign({}, row);
      this.editDialogVisible = true;
    },
    handleEditConfirm() {
      axios
        .put(`/api/userInfo/${this.editForm.id}`, this.editForm)
        .then((response) => {
          console.log(response);
          const index = this.userList.findIndex(
            (item) => item.id === response.data.id
          );
          Object.assign(this.userList[index], response.data);
          this.editDialogVisible = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    handleDelete(row) {
      axios
        .delete(`/api/user/${row.id}`)
        .then(() => {
          const index = this.userList.findIndex((item) => item.id === row.id);
          this.userList.splice(index, 1);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style>
</style>