<template>
  <div id="headerDefault" class="header-default">
    <b-navbar toggleable="sm" type="dark" variant="dark" sticky="true">
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-navbar-brand to="/user" class="mr-auto">MyServer</b-navbar-brand>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item v-show="is_loggedin" to="/projects">Projects</b-nav-item>
          <b-nav-item v-show="!is_loggedin" to="/tryaccess/login/user">Login</b-nav-item>
          <b-nav-item v-show="!is_loggedin" to="/tryaccess/signup/user">Signup</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-form>
            <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
            <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
          </b-nav-form>
          <b-nav-item-dropdown text="Lang" right id="lang-dropdown">
            <b-dropdown-item href="#">EN</b-dropdown-item>
            <b-dropdown-item href="#">ES</b-dropdown-item>
            <b-dropdown-item href="#">RU</b-dropdown-item>
            <b-dropdown-item href="#">FA</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item-dropdown right id="user-dropdown">
            <template slot="button-content">User</template>
            <b-dropdown-item to="/user">Profile</b-dropdown-item>
            <b-dropdown-item @click="logout">Sign Out</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import Axios from 'axios'
import { mapState } from 'vuex'
import * as types from '@/mutation_types'

export default {
  data () {
    return {
      is_loggedin: false
    }
  },
  computed: mapState([
    'token',
    'base_url'
  ]),
  methods: {
    isLoggedin () {
      const vm = this
      const check = async () => Axios.post(vm.base_url + '/api/loggedin', {
        token: vm.token
      }).then(resp => resp.data)
      check().then(res => vm.is_loggedin = res === 'valid')
    },
    logout () {
      this.$store.commit(types.USER_TOKEN, 'none')
      this.$router.push('/')
    }
  },
  created () {
    this.isLoggedin()
  },
  mounted () {
    this.$store.watch(
      (state, getters) => getters.current_token,
      (to, from) => this.isLoggedin() // eslint-disable-line no-unused-vars
    )
  }
}
</script>