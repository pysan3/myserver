import Vue from 'vue'
import Axios from 'axios'
import App from './App.vue'
import router from './router'
import store from './store'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.config.productionTip = false

router.beforeEach((to, from, next) => { // eslint-disable-line no-unused-vars
  if (to.matched.some(record => record.meta.requiredAuth)) {
    Axios.post(store.state.base_url + '/api/loggedin', {
      token: store.state.token
    }).then(resp => {
      if (resp.data === 'valid') {
        next()
      } else {
        next({
          name: 'tryaccess',
          params: {
            accessType: 'login',
            url: to.path.replace(/\//g, '-')
          }
        })
      }
    })
  }
  next()
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')