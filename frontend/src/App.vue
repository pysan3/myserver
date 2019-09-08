<template>
  <div id="app">
    <header><HeaderDefault/></header>
    <div class="small-size"><router-view/></div>
    <footer class="bg-dark fixed-bottom"><FooterDefault/></footer>
  </div>
</template>

<script>
import HeaderDefault from '@/components/HeaderDefault'
import FooterDefault from '@/components/FooterDefault'

export default {
  name: 'app',
  components: {
    HeaderDefault,
    FooterDefault
  }
}
</script>

<style lang="stylus">
#app
  font-family 'Avenir', Helvetica, Arial, sans-serif
  -webkit-font-smoothing antialiased
  -moz-osx-font-smoothing grayscale
  color #2c3e50
  text-align center
.small-size
  margin-bottom 122px
footer
  height 122px
.row
  margin 0px
</style>
