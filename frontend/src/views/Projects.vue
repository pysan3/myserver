<template>
  <div class="projects">
    <h2>{{ user_name }}</h2>
    <ul>
      <li v-for="project in projects" :key="project.name">
        <router-link v-bind:to="{name: 'directory', params: {project: project.name}}">{{ project.name }}</router-link>
        <button @click="manage_project('delete', project.name)">delete</button>
      </li>
      <li>
        <input type="text" v-model="new_project" @change="manage_project('create', new_project)">
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Axios from 'axios'

export default {
  data () {
    return {
      user_name: '',
      projects: [],
      new_project: ''
    }
  },
  computed: mapState([
    'token',
    'base_url'
  ]),
  methods: {
    load_projects () {
      Axios.post(this.base_url + '/api/loadproject', {
        token: this.token
      }).then(resp => {
        if (resp.data.valid === '1') {
          this.user_name = resp.data.user_name
          this.projects = resp.data.projects
          this.comment.splice()
        } else {
          alert('wrong access')
          this.$store.dispatch('logged_in', 'projects')
        }
      })
    },
    manage_project (command, name) {
      this.new_project = ''
      Axios.post(this.base_url + `/api/manageproject/${command}/${name}`, {
        token: this.token
      }).then(() => {
        this.load_projects()
      })
    }
  },
  created () {
    this.load_projects()
  }
}
</script>