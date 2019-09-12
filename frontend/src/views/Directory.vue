<template>
  <div class="directory container-fluid">
    <div class="row">
      <div class="inventory col-md-3">
        <div class="row no-gutters">
          <div class="col-lg-auto">
            <h3 class="text-left">{{ user_name }}-{{ project }}</h3>
          </div>
          <div class="col-lg-auto ml-auto align-self-end">
            <div class="d-flex justify-content-end">
              <button class="btn btn-outline-primary btn-sm" @click="new_file.type='file'">new file</button>
              <button class="btn btn-outline-primary btn-sm" @click="new_file.type='dir'">new dir</button>
              <input v-show="new_file.type!=='none'" type="text" value="" v-model="new_file.name" @change="newFile">
            </div>
          </div>
        </div>
        <div v-for="(item, index) in comment" :key="index">
          <this-file :comment="item"/>
        </div>
      </div>
      <div class="col-md-9">
        <div class="working-space">
          <div id="auto-save" class="file-navbar">
            <div class="d-flex">
              <div class="mr-auto align-self-end"><h3>{{ working_text[0].replace(/.*\//, '') }}</h3></div>
              <div v-show="autoSave!=='lost connection'"><button class="btn btn-outline-primary" @click="autoSave=!autoSave">{{ autoSave ? 'disable ' : ''}}auto save</button></div>
              <div v-show="autoSave==='lost connection'"><button class="btn btn-danger">{{ autoSave }}</button></div>
              <div v-show="autoSave!=='lost connection'"><button class="btn btn-outline-primary" @click="file_data = {}; working_text = ['', 0]">reload files</button></div>
              <div v-show="autoSave!=='lost connection'"><button class="btn btn-outline-primary" @click="saveFile()">save</button></div>
            </div>
          </div>
          <textarea id="file-data" class="file-data w-100" v-model="file_data[working_text[0]]" @change="working_text[1]+=1"></textarea>
        </div>
        <hr>
        <div class="terminal bg-dark text-white panel">
          <h4>terminal</h4>
          <input id="send-command" class="w-100" type="text" v-model="command[command.length-1]" @change="sendCommand" placeholder=">">
          <textarea id="result-data" class="terminal-data w-100" readonly v-model="result_data"></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Axios from 'axios'
import ThisFile from '@/components/ThisFile'

export default {
  components: {
    ThisFile
  },
  data () {
    return {
      project: this.$route.params.project,
      comment: [],
      new_file: {type: 'none', name: ''},
      user_name: '',
      working_text: ['', 0],
      autoSave: true,
      file_data: {'': ''},
      command: [''],
      result_data: '',
      connection: null
    }
  },
  computed: mapState([
    'token',
    'base_url',
    'ws_url'
  ]),
  methods: {
    load_files () {
      Axios.post(this.base_url + '/api/loadfile/' + this.project, {
        token: this.token
      }).then(resp => {
        if (resp.data.valid === '1') {
          this.user_name = resp.data.user_name
          this.comment = resp.data.comment
          this.comment.splice()
        }
      })
    },
    changeWorkingspace (from, to) {
      this.saveFile()
      if (Object.keys(this.file_data).includes(to)) {
        this.working_text = [to, 0]
      }
      else {
        Axios.post(this.base_url + '/api/userfile/' + to, {
          token: this.token
        }).then(resp => {
          this.file_data[to] = resp.data
          this.working_text = [to, 0]
        })
      }
    },
    saveFile () {
      if (this.autoSave && this.working_text[0] !== '' && this.working_text[1]) {
        Axios.post(this.base_url + '/api/fileupload/' + this.working_text[0], {
          token: this.token,
          data: this.file_data[this.working_text[0]]
        })
      }
    },
    newFile () {
      if (this.new_file.name.length !== 0) {
        const command = {'file': 'echo "" >', 'dir': 'mkdir'}
        this.connection.send(JSON.stringify({
          token: this.token,
          command: `${command[this.new_file.type]} ${this.new_file.name}`
        }))
        this.new_file.type = 'none'
        this.new_file.name = ''
      }
    },
    ws_connection () {
      const vm = this
      this.connection = new WebSocket(this.ws_url + '/ws/terminal')
      this.connection.onopen = () => {
        vm.connection.send(JSON.stringify({
          token: vm.token,
          project: vm.project
        }))
      }
      this.connection.onmessage = event => {
        const data = JSON.parse(event.data)
        vm.result_data += data.result
        vm.load_files()
      }
      this.connection.onclose = () => {
        vm.connection.close()
        vm.connection = null
        vm.autoSave = 'lost connection'
      }
    },
    sendCommand () {
      const vm = this
      let new_command = '!!', i = 1
      while (new_command === '!!' && vm.command.length >= i) {
        new_command = vm.command[vm.command.length-(i++)]
      }
      this.connection.send(JSON.stringify({
        token: vm.token,
        command: new_command
      }))
      this.result_data += `> ${new_command}\n`
      this.command.push('')
    }
  },
  created () {
    this.load_files()
    this.working_text = ['', 0]
  },
  mounted () {
    this.$store.watch(
      (state, getters) => getters.current_fileID,
      (to, from) => {
        this.changeWorkingspace(from, to)
      }
    )
    this.ws_connection()
  },
  updated () {
    const result = document.getElementById('result-data')
    result.scrollTop = result.scrollHeight
  },
  beforeRouteLeave (to, from, next) {
    this.saveFile()
    if (this.connection !== null) {
      if (!this.autoSave) {
        const ans = window.confirm('changes not been saved!!')
        if (ans) next()
        else next(false)
      } else {
        next()
      }
    }
  },
  beforeDestroy () {
    if (this.connection !== null) {
      this.connection.close()
    }
  }
}
</script>

<style lang="stylus" scoped>
hr
  margin 4px 0px
h3
  margin 5px 0px 0px 0px
.directory
  padding 0px 8px
.working-space
  .file-data
    height 50vh
.terminal
  .terminal-data
    height 15vh
</style>