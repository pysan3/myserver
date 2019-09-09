<template>
  <div id="todolist" class="row">
    <div v-for="list in Object.keys(todolist)" :key="list" class="col-md-4 col-lg-2">
      <table class="table">
        <thead class="thead-light"><tr><th>
          <div class="d-flex">
            <div class="flex-grow-1">{{ list }}</div>
            <div class="dropdown">
              <button type="button" id="dropdownList" class="btn btn-secondary dropdown-toggle btn-sm" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"></button>
              <div class="dropdown-menu" aria-labelledby="dropdownList">
                <a class="dropdown-item" @click="delete_list(list)">delete</a>
                <a class="dropdown-item" @click="show_isDone(list)">{{ showAll[list]?'hide':'show' }} done items</a>
              </div>
            </div>
          </div>
        </th></tr></thead>
        <tr v-for="el in todolist[list]" :key="el.name" v-show="!el.isDone || showAll[list]"><th>
          <div class="d-flex">
            <div class="mr-auto">{{ el.name }}</div>
            <div><button v-show="!el.isDone" class="btn btn-outline-danger btn-sm" @click="done_element(list, el)">Done!</button></div>
            <div><button v-show="el.isDone" class="btn btn-outline-info btn-sm" @click="done_element(list, el)">not done</button></div>
            <div><button v-show="el.isDone" class="btn btn-outline-danger btn-sm" @click="delete_element(list, el)">delete</button></div>
          </div>
        </th></tr>
        <tr><th>
          <button v-show="new_element.show!==`element-${list}`" type="button" class="btn btn-outline-primary" @click="new_element.show=`element-${list}`">add element</button>
          <input id="createElement" v-show="new_element.show===`element-${list}`" type="text" placeholder="name of new element" v-model="new_element.name" @change="create_element(list)">
        </th></tr>
      </table>
    </div>
    <div class="col-md-4 col-lg-2">
      <button v-show="new_element.show!=='list'" show="button" class="btn btn-outline-primary" @click="new_element.show='list'">add list</button>
      <input id="createList" v-show="new_element.show==='list'" show="text" placeholder="name of new list" v-model="new_element.name" @change="create_list()">
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Axios from 'axios';

export default {
  data () {
    return {
      new_element: {'show': '', 'name': ''},
      todolist: {},
      showAll: {},
    }
  },
  computed: mapState([
    'token',
    'base_url'
  ]),
  methods: {
    load_list () {
      Axios.post(this.base_url + '/api/todolist/load', {
        token: this.token
      }).then(resp => {
        this.todolist = resp.data
        Object.keys(this.todolist).forEach(list => {
          this.showAll[list] = 0
        })
      })
    },
    create_list () {
      if (!(this.new_element.name in Object.keys(this.todolist))) {
        Axios.post(this.base_url + '/api/todolist/createlist', {
          token: this.token,
          list_name: this.new_element.name
        }).then(() => {
          this.todolist[this.new_element.name] = []
        })
      }
      this.new_element = {'show': '', 'name': ''}
    },
    create_element (list) {
      Axios.post(this.base_url + '/api/todolist/createelement', {
        token: this.token,
        list_name: list,
        name: this.new_element.name
      }).then(() => {
        this.todolist[list].push({
          'name': this.new_element.name,
          'isDone': false
        })
        this.new_element = {'show': '', 'name': ''}
      })
    },
    delete_list (list) {
      Axios.post(this.base_url + '/api/todolist/deletelist', {
        token: this.token,
        list_name: list,
      }).then(() => {
        this.load_list()
      })
    },
    delete_element (list, el) {
      Axios.post(this.base_url + '/api/todolist/deleteelement', {
        token: this.token,
        list_name: list,
        name: el.name
      }).then(() => {
        this.todolist[list] = this.todolist[list].filter(n => n.name !== el.name)
      })
    },
    done_element (list, el) {
      Axios.post(this.base_url + '/api/todolist/doneelement', {
        token: this.token,
        list_name: list,
        name: el.name
      }).then(() => {
        el.isDone = !el.isDone
      })
    },
    show_isDone (list) {
      this.showAll[list] ^= 1
      this.$forceUpdate()
    }
  },
  mounted () {
    this.load_list()
  }
}
</script>