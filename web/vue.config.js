const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  publicPath: "./",
  assetsDir: "static",
  outputDir: "dist",
  transpileDependencies: true,
  lintOnSave: false, //关闭eslint
  devServer: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true, //是否跨域
        pathRewrite: { "^/api": "" },
      },
    },
  },
});
