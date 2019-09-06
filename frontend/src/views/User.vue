<template>
  <div>
    <p>Home page</p>
    <h1>class for css, id for js</h1>
    <p>Random number from backend: {{ randomNumber }}</p>
    <button @click="getRandom">New random number</button>
    <router-link to="/about"><a>about</a></router-link>
    <br>
    <router-link to="/projects"><a>your projects</a></router-link>
    <ToDoList/>
  </div>
</template>

<script>
import Axios from 'axios'
import { mapState } from 'vuex'
import ToDoList from '@/components/ToDoList'

export default {
  components: {
    ToDoList
  },
  data () {
    return {
      randomNumber: 0
    }
  },
  computed: mapState([
    'base_url'
  ]),
  methods: {
    getRandom () {
      Axios.get(this.base_url + '/api/random').then(response => {
        this.randomNumber = response.data.randomNumber
      })
    }
  },
  created () {
    this.$store.dispatch('logged_in', 'user')
    this.getRandom()
  }
}
</script>
