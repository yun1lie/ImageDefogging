<template>
  <el-footer height="80px">
    <div class="bottom-container">
      <div class="system-info">
        <h3>系统说明</h3>
        <p>
          该系统使用暗通道去雾算法对腹腔镜图像进行去雾处理，提高图像清晰度。
        </p>
      </div>
      <div class="terms">
        <h3>服务条款及隐私政策</h3>
        <ul>
          <li>本系统严格遵守国家法律法规，保护用户个人信息安全。</li>
          <li>用户在使用本系统时需遵守以下服务条款：</li>
          <ul>
            <li>不得用于非法用途。</li>
            <li>不得破坏系统运行。</li>
            <li>不得侵犯他人权益。</li>
          </ul>
        </ul>
      </div>
      <div class="contact">
        <h3>联系方式</h3>
        <p>邮箱：support@example.com</p>
        <p>电话：010-12345678</p>
      </div>
    </div>
  </el-footer>
</template>

<style scoped>
.bottom-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.system-info h3,
.terms h3,
.contact h3 {
  margin-bottom: 10px;
  font-weight: bold;
  font-size: 18px;
}

.system-info p,
.terms ul li {
  font-size: 14px;
  line-height: 20px;
}

.terms ul {
  list-style: none;
  padding-left: 0;
  margin-top: 10px;
}

.terms ul ul {
  list-style: disc;
  margin-top: 5px;
  margin-left: 20px;
}

.contact p {
  font-size: 14px;
  line-height: 20px;
  margin-top: 5px;
}

.contact p:first-of-type {
  margin-top: 0;
}
</style>