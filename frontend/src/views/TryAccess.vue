<template>
  <div>
    <h2>{{ accessTypes[accessID] }}</h2>
    <input type="text" placeholder="Username" v-model="user_name">
    <input type="password" placeholder="Password" v-model="user_password">
    <input v-show="!accessID" type="text" placeholder="github name" v-model="github_name">
    <button @click="tryAccess">{{ accessTypes[accessID] }}!!</button>
    <p>{{ msg[accessID^1] }}</p>
    <button @click="accessOpposite">{{ accessTypes[accessID^1] }}</button>
    <br>
    <p>user_name {{ user_name }}</p>
    <p>password {{ user_password }}</p>
  </div>
</template>

<script>
import Axios from 'axios'
import { mapState } from 'vuex'
import * as types from '../src/mutation_types'
export default {
  data () {
    return {
      accessTypes: ['signup', 'login'],
      accessID: Number(this.$route.params.accessType === 'login'),
      url: this.$route.params.url.replace(/-/g, '/'),
      user_name: '',
      user_password: '',
      github_name: '',
      msg: ['make a new account', 'already have an account']
    }
  },
  computed: mapState([
    'base_url'
  ]),
  watch: {
    '$route' (to, _) { // eslint-disable-line no-unused-vars
      this.accessID = Number(to.params.accessType === 'login')
    }
  },
  methods: {
    tryAccess () {
      if (this.user_name.length * this.user_password.length === 0) {
        alert('should not be zero charactors')
        return
      }
      Axios.post(this.base_url + '/api/' + this.accessTypes[this.accessID], {
        user_name: this.user_name,
        user_password: this.user_password,
        github_name: this.github_name
      }).then(response => {
        const responseID = response.data.user_id - 0
        if (responseID !== -1 && response.data.isFound-0 === 1) {
          this.$store.commit(types.USER_TOKEN, response.data.token)
          this.$router.push(this.url)
        } else {
          alert(response.data.msg)
        }
      })
    },
    accessOpposite () {
      this.$router.push({
        name: 'tryaccess',
        params: {
          accessType: this.accessTypes[-1 * (this.accessID - 1)]
        }
      })
    }
  },
  created () {
    if (this.accessID === 0 && this.$route.params.accessType !== 'signup') {
      alert('url broken')
      this.$router.push('/')
    }
  }
}
</script>

<style lang="stylus" scoped>
h1, h2 {
  font-weight: normal
}
ul {
  list-style-type: none
  padding: 0
}
li {
  display: inline-block
  margin: 0 10px
}
a {
  color: #42b983
}
.signup {
  margin-top: 20px

  display: flex
  flex-flow: column nowrap
  justify-content: center
  align-items: center
}
input {
  margin: 10px 0
  padding: 10px
}
</style>
