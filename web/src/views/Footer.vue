<template>
  <el-footer class="footer">
    <div class="container">
      <section class="system-info">
        <h3>系统说明</h3>
        <p>
          该系统使用暗通道去雾算法对腹腔镜图像进行去雾处理，提高图像清晰度。
        </p>
      </section>
      <section class="terms">
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
      </section>
      <section class="contact">
        <h3>联系方式</h3>
        <address>
          <p>
            邮箱：<a href="mailto:support@example.com">support@example.com</a>
          </p>
          <p>电话：<a href="tel:010-12345678">010-12345678</a></p>
        </address>
      </section>
    </div>
  </el-footer>
</template>

<style scoped>
.footer {
  background-color: #f5f5f5;
  padding: 20px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.system-info,
.terms,
.contact {
  flex-basis: 30%;
  margin-bottom: 20px;
}

.system-info h3,
.terms h3,
.contact h3 {
  margin: 0 0 10px;
  font-weight: bold;
  font-size: 1.2rem;
}

.system-info p,
.terms ul li,
.contact p {
  font-size: 1rem;
  line-height: 1.5;
}

.terms ul,
.terms ul ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.terms ul ul {
  margin-top: 5px;
  margin-left: 20px;
}

.terms ul li:before {
  content: "•";
  margin-right: 5px;
  color: #999;
}

.contact p a {
  color: #666;
}

.contact p a:hover {
  color: #333;
  text-decoration: none;
}

.contact p:first-of-type {
  margin-top: 0;
}
</style>

<script>
export default {
  name: "Footer",
};
</script>
