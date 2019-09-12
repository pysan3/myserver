import Vue from 'vue'
import Vuex from 'vuex'
import * as types from '@/mutation_types'
Vue.use(Vuex)

const state = {
  token: 'none',
  base_url: 'http://127.0.0.1:5042',
  ws_url: 'ws://127.0.0.1:5042',
  current_fileID: ''
}

const getters = {
  current_fileID (state) {
    return state.current_fileID
  },
  current_token (state) {
    return state.token
  }
}

const mutations = {
  [types.USER_TOKEN] (state, token) {
    state.token = token
  },
  [types.CURRENT_FILEID] (state, id) {
    state.current_fileID = id
  }
}

export default new Vuex.Store({
  state,
  getters,
  mutations
})
