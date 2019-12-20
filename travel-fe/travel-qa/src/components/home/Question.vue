<template>
  <div class="question">
    <div class="question-header col-md-12">
      <p class="question-header-menu">Question about</p>
      <p class="question-header-menu">Region</p>
      <p class="question-header-menu">Category</p>
    </div>
    <div class="question-content col-md-12">
      <p class="question-title">Title of the question</p>
      <p class="question-des">Question details <br/> aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</p>
      <div class="question-review">
        <i class="fa fa-heart" ></i> 10
        <i class="fa fa-comment" ></i> 11
      </div>
      <div class="question-add-comment">
        <input type="text" placeholder="Answer this question">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Question',
  data () {
    return {
      loading: false
    }
  },

  created () {
  },

  methods: {

  }
}
</script>

<style lang="css" scoped>
.question {
  width: 100%;
  border: 1px solid #ccc;
  margin-bottom: 20px;
  text-align: left;
}

.question-header {
  display: flex;
}

.question-header-menu {
  margin: 10px 20px 10px 0;
}

.question-content {
  /* text-align: left; */
}

.question-title {
  font-size: 18px;
  font-weight: bold;
}

.question-des {
  width: 100%;
  word-break: break-all;
}

.question-review {
  font-size: 20px;
}

.question-add-comment {
  margin-bottom: 5px;
}

.question-add-comment input {
  width: 100%;
  height: 40px;
  padding-left: 10px;
}
</style>
