<template>
  <div class="layout">
    <!-- 头部区域 -->
    <el-header height="80px" style="background-color: #fafafa">
      <div class="logo">Logo</div>
      <div class="nav">
        <el-menu :default-active="$route.path" mode="horizontal">
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/about">关于我们</el-menu-item>
          <el-menu-item index="/contact">联系我们</el-menu-item>
        </el-menu>
      </div>
      <div class="user-info">
        <el-dropdown>
          <span class="el-dropdown-link">
            <i class="el-icon-user"></i> 用户名<i
              class="el-icon-arrow-down el-icon--right"
            ></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>个人信息</el-dropdown-item>
            <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </el-header>
    <!-- 主要区域 -->
    <el-main>
      <div class="main-container">
        <!-- 图像上传模块 -->
        <div class="upload">
          <el-upload class="upload-demo" action="#">
            <el-button type="primary" icon="el-icon-upload"
              >点击上传图片</el-button
            >
          </el-upload>
        </div>
        <!-- 去雾效果预览模块 -->
        <div class="preview">
          <img src="https://picsum.photos/400/300" alt="preview image" />
        </div>
        <!-- 参数调节模块 -->
        <div class="parameters">
          <el-form label-width="100px">
            <el-form-item label="雾的强度">
              <el-slider v-model="fogIntensity" :min="0" :max="100"></el-slider>
            </el-form-item>
            <el-form-item label="透视度">
              <el-slider v-model="perspective" :min="0" :max="100"></el-slider>
            </el-form-item>
            <el-form-item label="光照">
              <el-slider v-model="lighting" :min="0" :max="100"></el-slider>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </el-main>
    <!-- 底部区域 -->
    <el-footer height="80px" style="background-color: #ebebeb">
      <div class="bottom-container">
        <div class="system-info">系统说明</div>
        <div class="terms">服务条款 | 隐私政策</div>
        <div class="contact">联系方式</div>
      </div>
    </el-footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      fogIntensity: 50,
      perspective: 50,
      lighting: 50,
    };
  },
  methods: {
    handleLogout() {
      // 执行退出登录逻辑
    },
  },
};
</script>

<style scoped>
.layout {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.el-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 1px 3px #ebebeb;
}
.logo {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}
.nav {
  display: flex;
  justify-content: center;
}
.user-info {
  display: flex;
  align-items: center;
}
.el-main {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
}
.main-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.upload {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
}
.preview {
  flex: 3;
  margin: 0 20px;
  border: 1px solid #ebebeb;
}
.parameters {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
}
.el-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 20px;
}
.bottom-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
  color: #999;
}
.system-info {
  font-size: 14px;
  font-weight: bold;
}
.terms,
.contact {
  font-size: 12px;
  cursor: pointer;
}
</style>
