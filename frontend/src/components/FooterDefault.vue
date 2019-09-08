<template>
  <div id="footerDefault" class="footer-default fixed-bottom">
    <div id="githubKusa">
      <svg id="draw-kusa" width="722" heigh="122" class="onright"></svg>
    </div>
  </div>
</template>

<script>
import Axios from 'axios'
import { mapState } from 'vuex'
import $ from 'jquery'

export default {
  data () {
    return {
      github_name: ''
    }
  },
  computed: mapState([
    'token',
    'base_url'
  ]),
  methods: {
    loadKusa () {
      Axios.post(this.base_url + '/api/kusa', {
        token: this.token
      }).then(resp => {
        this.github_name = resp.data.github_name
        let html = '', column = 22, month = null
        resp.data.garden.forEach(g => {
          if (g.day === 0) {
            column += 13
            if (g.date.split('-')[1] !== month) {
              month = g.date.split('-')[1]
              html += `<text width="10" height="10" x="${column}" y="18" fill="white">${parseInt(month)}</text>`
            }
          }
          html += `<rect fill="${g.color}" width="10" height="10" x="${column}" y="${g.day*13+19}" class="kusa-day"><title>${g.count} contributions on ${g.date}</title></rect>`
        })
        document.getElementById('draw-kusa').innerHTML += html + `
        <text width="10" height="10" x="33" y="45" text-anchor="end" fill="white">Mon</text>
        <text width="10" height="10" x="33" y="71" text-anchor="end" fill="white">Wed</text>
        <text width="10" height="10" x="33" y="97" text-anchor="end" fill="white">Fri</text>`
      })
      $('[data-toggle="tooltip"]').tooltip()
    }
  },
  mounted () {
    this.loadKusa()
  }
}
</script>

<style lang="stylus" scoped>
#githubKusa
  position relative
  overflow hidden
  width 722px
  height 122px
  float right
  margin 0px 12px

.onright
  position absolute
  right 0px
</style>