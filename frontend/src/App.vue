<template>
  <div id="app">
    <HeaderDefault/>
    <router-view/>
    <FooterDefault/>
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
  text-align center
  color #2c3e50
</style>
