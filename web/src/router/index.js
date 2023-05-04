import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);
const router = new VueRouter({
  mode: "hash",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      component: () => import("@/views/Home.vue"),
    },
    {
      path: "/login",
      component: () => import("@/views/login.vue"),
    },
    {
      path: "/userHome",
      component: () => import("@/views/userHome.vue"),
    },
    {
      path: "/register",
      component: () => import("@/views/register.vue"),
    },
    {
      path: "/UserInfo",
      component: () => import("@/views/UserInfo.vue"),
    },
    {
      path: "/userMan",
      component: () => import("@/views/userMan.vue"),
    },
  ],
});

export default router;
