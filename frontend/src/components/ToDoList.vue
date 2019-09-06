<template>
  <div id="todolist" class="row">
    <div v-for="list in Object.keys(todolist)" :key="list" class="col-md-4 col-lg-2">
      <table class="table">
        <thead class="thead-light"><tr><th>{{ list }}</th></tr></thead>
        <tr v-for="el in todolist[list]" :key="el.name" v-show="!el.isDone"><th>{{ el.name }}</th></tr>
        <tr><th>
          <button v-show="new_element.show!==`element-${list}`" type="button" class="btn btn-outline-primary" @click="new_element.show=`element-${list}`">add element</button>
          <input v-show="new_element.show===`element-${list}`" type="text" placeholder="name of new element" v-model="new_element.name" @change="create_element(list)">
        </th></tr>
      </table>
    </div>
    <div class="col-md-4 col-lg-2">
      <button v-show="new_element.show!=='list'" show="button" class="btn btn-outline-primary" @click="new_element.show='list'">add list</button>
      <input v-show="new_element.show==='list'" show="text" placeholder="name of new list" v-model="new_element.name" @change="create_list">
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
      todolist: {}
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
      })
    },
    create_list () {
      Axios.post(this.base_url + '/api/todolist/createlist', {
        token: this.token,
        list_name: this.new_element.name
      }).then(() => {
        this.todolist[this.new_element.name] = []
        this.new_element = {'show': '', 'name': ''}
      })
    },
    create_element (list_name) {
      Axios.post(this.base_url + '/api/todolist/createelement', {
        token: this.token,
        list_name: list_name,
        name: this.new_element.name
      }).then(() => {
        this.todolist[list_name].push({
          'name': this.new_element.name,
          'isDone': false
        })
        this.new_element = {'show': '', 'name': ''}
      })
    }
  },
  mounted () {
    this.load_list()
  }
}
</script>