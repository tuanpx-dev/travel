<template>
  <div class="container">
    <Header />
    <router-view/>
  </div>
</template>

<script>
import Header from './header/header'
import Home from './home/Home'
import DetailQuestion from './detailQuestion/detailQuestion'
export default {
  name: 'View',
  components: {
    Header,
    Home,
    DetailQuestion
  },
  data () {
    return {
    }
  }
}
</script>

<style lang="css" scoped>

</style>
