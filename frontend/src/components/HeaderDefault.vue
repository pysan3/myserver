<template>
  <header id="header">
    <nav class="navbar navbar-dark bg-dark">
      <router-link class="nav-item nav-link navbar-brand" to="/user">MyServer</router-link>
      <button type="button" class="navbar-toggler" data-toggle="collapse" data-target="#Navber" aria-controls="Navber" aria-expanded="false" aria-label="ナビゲーションの切替">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="Navbar">
        <router-link class="nav-item nav-link" to="/projects">Projects</router-link>
        <div v-if="isLoggedin()">
          <router-link class="nav-item nav-link" to="/projects">Projects</router-link>
        </div>
        <div v-else>
          <router-link class="nav-item nav-link" to="/tryaccess/login/user">Login</router-link>
          <router-link class="nav-item nav-link" to="/tryaccess/signup/user">Signup</router-link>
        </div>
        <!-- <form class="form-inline my-2 my-lg-0">
          <input type="search" class="form-control mr-sm-2" placeholder="検索..." aria-label="検索...">
          <button type="submit" class="btn btn-outline-success my-2 my-sm-0">検索</button>
        </form> -->
      </div>
    </nav>
  </header>
</template>

<script>
import Axios from 'axios'
import { mapState } from 'vuex'

export default {
  computed : mapState([
    'token',
    'base_url'
  ]),
  methods: {
    isLoggedin () {
      const vm = this
      const check = async () => Axios.post(cm.base_url + '/api/loggedin', {
        token: cm.token
      }).then(resp => resp.data)
      check().then(res => res === 'valid')
    }
  }
}
</script>