import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/user', component: 'User' },
  { path: '/tryaccess/:accessType/:url', component: 'TryAccess' },
  { path: '/projects', component: 'Projects' },
  { path: '/directory/:project', component: 'Directory' },
  { path: '*', component: 'HelloWorld' },
];

const routes = routerOptions.map(route => {
  return {
    ...route,
    name: `${route.component}`.toLowerCase(),
    component: () => import(`@/views/${route.component}.vue`)
  };
});

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});
