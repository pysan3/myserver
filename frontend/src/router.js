import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

const routerOptions = [
  { path: '/', component: 'Home', requiredAuth: false },
  { path: '/user', component: 'User', requiredAuth: true },
  { path: '/tryaccess/:accessType/:url', component: 'TryAccess', requiredAuth: false },
  { path: '/projects', component: 'Projects', requiredAuth: true },
  { path: '/directory/:project', component: 'Directory', requiredAuth: true },
  { path: '*', component: 'HelloWorld', requiredAuth: false },
  { path: '/user', component: 'User', requiredAuth: true },
]

const routes = routerOptions.map(route => ({
  path: route.path,
  name: `${route.component}`.toLowerCase(),
  component: () => import(`@/views/${route.component}.vue`),
  meta: {
    requiredAuth: route.requiredAuth
  }
}))

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})