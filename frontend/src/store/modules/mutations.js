import * as types from '@/store/modules/mutation_types'

export default {
  [types.USER_TOKEN] (state, token) {
    state.token = token
  },
  [types.CURRENT_FILEID] (state, id) {
    state.current_fileID = id
  }
}