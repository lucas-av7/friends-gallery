import { createRouter, createWebHistory } from "vue-router";
import AdminView from "../views/AdminView.vue";
import HomeView from "../views/HomeView.vue";
import PhotoView from "../views/PhotoView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", component: HomeView },
    { path: "/photo/:id", component: PhotoView },
    { path: "/admin", component: AdminView },
  ],
});

export default router;
