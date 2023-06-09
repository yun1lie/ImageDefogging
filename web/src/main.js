import Vue from "vue";
import App from "./App.vue";
import router from "@/router";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";

import * as echarts from 'echarts';

Vue.prototype.$echarts = echarts
// import "@/theme/index.css";

Vue.config.productionTip = false;
Vue.use(ElementUI);

new Vue({
  render: (h) => h(App),
  router,
}).$mount("#app");