<template>
  <div class="profile">
    <div class="avartar-name">

    </div>

    <div class="note-des">

    </div>

    <div class="review-user">
      <div class="change-review">
        <p class="change-title">Name</p>
        <p v-if="true" class="user-name">hâhhaha</p>
        <input v-else type="text">
        <p>icon edit</p>
      </div>
    </div>

    <div class="interest">
      <p>title</p>
      <div class="category">
        <p>Category</p>
        <div class="list-category">

        </div>
      </div>
      <div class="area">

      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile',

  components: {
  },

  data () {
    return {

    }
  },

  methods: {

  }
}
</script>

<style lang="css" scoped>
</style>
