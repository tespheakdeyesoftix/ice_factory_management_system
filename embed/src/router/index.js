import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import authRoutes from './auth';

const routes = [
  {
	path: "/",
	name: "Home",
	component: Home,
  },
  {
	path: "/server-report",
	name: "ServerReport",
  component: () => import('@/views/server-report/ServerReport.vue'), 
  },
  ...authRoutes,
];

const router = createRouter({
  history: createWebHistory("/embed/"),
  routes,
});

export default router;
