<template>
  <div class="layout">
    <!-- 头部区域 -->
    <Header />
    <!-- 主要区域 -->
    <Main />
    <!-- 底部区域 -->
    <Footer />
  </div>
</template>

<script>
import Header from "./Header";
import Main from "./Main";
import Footer from "./Footer";

export default {
  components: {
    Header,
    Main,
    Footer,
  },
};
</script>

<style scoped>
.layout {
  height: 100%;
  display: grid;
  grid-template-rows: 80px auto 80px;
}

.el-footer,
.el-header {
  padding: 0 20px;
  box-shadow: 0 1px 3px #ebebeb;
}

.el-header {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  background-color: #fafafa;
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

.main-container {
  display: grid;
  grid-template-columns: 1fr 3fr 1fr;
}

.upload,
.parameters {
  padding: 20px;
  box-sizing: border-box;
}

.preview {
  margin: 0 20px;
  border: 1px solid #ebebeb;
}

.bottom-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  align-items: center;
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
