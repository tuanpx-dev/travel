<template>
  <div class="container">
    <Header />
    <router-view/>
  </div>
</template>

<script>
import Header from './header/header'
export default {
  name: 'View',
  components: {
    Header
  },
  data () {
    return {
    }
  }
}
</script>

<style lang="css" scoped>
.container {
  padding: 0;
}
</style>
