import Vue from 'vue'
import Vuex from 'vuex'
import state from '@/store/modules/state'
import getters from '@/store/modules/getters'
import mutations from '@/store/modules/mutations'
import actions from '@/store/modules/actions'

Vue.use(Vuex)

export default new Vuex.Store({
  state,
  getters,
  mutations,
  actions
})
