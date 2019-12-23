<template>
  <div class="row header">
    <div class="col-md-3">
      <div>
        <p class="logo">TravelQA</p>
        <button class="button-ask" @click="addAsk()">Ask</button>
      </div>
    </div>
    <div class="col-md-6"></div>
    <div class="col-md-3"></div>

    <modal name="create-new-ask">
      create-new-a-ask
    </modal>
  </div>
</template>

<script>
export default {
  name: 'Header',

  data () {
    return {}
  },

  methods: {
    addAsk () {
      this.$modal.show('create-new-ask')
    }
  }
}
</script>

<style lang="css" scoped>
.header {
  margin-top: 20px;
}

.header .col-md-3{
  z-index: 100;
}

.logo {
  font-size: 22px;
  font-weight: 500;
  color: #495057;
  border: 1px solid #495057;
  padding: 20px 0px;
  border-radius: 20px;
  width: 60%;
  margin: 0 auto;
}

.button-ask {
  padding: 5px 25px;
  border-radius: 20px;
  border: 1px solid #ccc;
  background-color: white;
  font-size: 24px;
  font-weight: 800;
  outline: none;
  margin-top: 15px;
}
</style>
