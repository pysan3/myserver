<template>
  <div id="app">
    <header class="sticky-top"><HeaderDefault/></header>
    <div class="small-size"><router-view/></div>
    <FooterDefault class="fixed-bottom"/>
  </div>
</template>

<script>
import HeaderDefault from '../src/components/HeaderDefault'
import FooterDefault from '../src/components/FooterDefault'

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
