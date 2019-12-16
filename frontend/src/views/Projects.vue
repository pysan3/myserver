<template>
  <div class="projects">
    <div class="row mt-4">
      <div class="col-lg-2 d-none d-lg-block">
        <div class="card card-body bg-light">
          <h2>{{ user_name }}</h2>
        </div>
      </div>
      <div class="col-lg-10">
        <div class="row no-gutters">
          <div class="col-12">
            <div class="d-flex" style="min-height: 50px">
              <button class="btn btn-outline-success" @click="new_project.type='create'">Create</button>
              <button class="btn btn-outline-dark" @click="new_project.type='search'">Search</button>
              <div v-show="new_project.type==='create'" class="flex-grow-1 card card-body p-1">
                <input class="form-control" type="text" v-model="new_project.name" placeholder="new project name" @change="manage_project('create', new_project.name)">
              </div>
              <div v-show="new_project.type==='search'" class="flex-grow-1 card card-body p-1 container-fluid">
                <div class="row no-gutters">
                  <input class="col-12 col-md-8 form-control" type="text" v-model="new_project.name" placeholder="search project">
                  <div class="col-12 col-md-4 d-flex">
                    <input class="form-control flex-grow-1" type="text" v-model="new_project.option" placeholder="option">
                    <button class="btn btn-dark" @click="search()">Find</button>
                  </div>
                </div>
              </div>
              <div class="d-flex dropdown">
                <button type="button" id="sort" class="btn btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Sort</button>
                <div class="dropdown-menu dropdown-menu-right" aria-labelledby="sort">
                  <a class="dropdown-item" @click="sortList('name')">name</a>
                </div>
              </div>
            </div>
          </div>
          <div class="col-12 col-lg-6" v-for="project in projects" :key="project.name" v-show="project_show[project.name]">
            <div class="card card-body bg-light project d-flex">
              <router-link v-bind:to="{name: 'directory', params: {project: project.name}}"><h3>{{ project.name }}</h3></router-link>
              <button class="ml-auto btn btn-danger" @click="manage_project('delete', project.name)">delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>
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
      project_show: {},
      new_project: {
        type: 'search',
        name: '',
        option: ''
      },
      current_sort: ''
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
          this.projects.forEach(project => {
            this.project_show[project.name] = true
          })
          this.current_sort = 'name'
        }
      })
    },
    manage_project (command, name) {
      this.new_project.name = ''
      Axios.post(this.base_url + `/api/manageproject/${command}/${name}`, {
        token: this.token
      }).then(() => {
        this.load_projects()
      })
    },
    search () {
      const searchOption = new RegExp(this.new_project.name, this.new_project.option)
      this.projects.forEach(project => {
        this.project_show[project.name] = searchOption.test(project.name)
      })
      this.$forceUpdate()
    },
    sortList (type) {
      if (type !== this.current_sort) {
        let cmpFunc = (a, b) => (a < b ? -1 : 1)
        if (type === 'name') cmpFunc = (a, b) => (a.name < b.name ? -1 : 1)
        this.projects.sort(cmpFunc)
      } else {
        this.projects.reverse()
      }
      this.current_sort = type
      this.$forceUpdate()
    }
  },
  created () {
    this.load_projects()
  }
}
</script>

<style lang="stylus" scoped>
.project
  margin 10px 15px
</style>