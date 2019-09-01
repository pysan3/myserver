<template>
  <footer>
    <div id="githubKusa">
      <svg id="draw-kusa" width="722" heigh="122" class="onright"></svg>
    </div>
  </footer>
</template>

<script>
import Axios from 'axios'
import { mapState } from 'vuex'

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
              html += `<text width="10" height="10" x="${column}" y="12">${parseInt(month)}</text>`
            }
          }
          html += `<rect fill="${g.color}" width="10" height="10" x="${column}" y="${g.day*13+13}" class="kusa-day ${g.date} ${g.count}"></rect>`
        })
        document.getElementById('draw-kusa').innerHTML += html + `
        <text width="10" height="10" x="33" y="39" text-anchor="end">Mon</text>
        <text width="10" height="10" x="33" y="65" text-anchor="end">Wed</text>
        <text width="10" height="10" x="33" y="91" text-anchor="end">Fri</text>`
      })
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

.onright
  position absolute
  right 0px
</style>