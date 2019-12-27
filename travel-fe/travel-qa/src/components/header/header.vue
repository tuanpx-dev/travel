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

    <modal
      name="create-new-ask"
      width="60%"
      height="500px"
      :scrollable="false"
      :clickToClose="false">
      <h3 class="title-popup-ask">AskQuestion</h3>

      <div class="popup-note">
        <p>Tips for getting answers</p>
        <p>1</p>
        <p>2</p>
        <p>3</p>
      </div>

      <div class="ask-title">
        <div class="ask-user">
          <img src="https://scontent.fhan2-4.fna.fbcdn.net/v/l/t1.0-9/79718560_558443374887450_3199243511551492096_n.jpg?_nc_cat=100&_nc_ohc=wwxTklQV7QgAQkI9nPX_W92osAYeK6NMO3Sk0yYTImrPEDpKoETFGrQQg&_nc_ht=scontent.fhan2-4.fna&oh=4484df51e86cb97abeb83d0f70910f0e&oe=5E781D35" alt="">
          <p>{{ user.username }} has a question</p>
        </div>
        <input type="text" placeholder="Enter the title of the question here" v-model="titleQuestion">
      </div>

      <div class="ask-deatail">
        <textarea placeholder="Enter your question details here" rows="4" cols="50" v-model="detailQuestion">
        </textarea>
      </div>

      <div class="action-ask">
        <button class="action-cancel" @click="closeASK"> Cancel</button>
        <button class="action-create" @click="createASK"> Question </button>
      </div>
    </modal>
  </div>
</template>

<script>
import { EventBus } from '../../eventBus'
import request from '../../../request/request'
import { URL } from '../../api/URL'

export default {
  name: 'Header',

  data () {
    return {
      titleQuestion: '',
      detailQuestion: '',
      user: {}
    }
  },

  created () {
    this.user = JSON.parse(localStorage.getItem('user')).data.user
  },

  methods: {
    closeASK () {
      this.$modal.hide('create-new-ask')
    },

    addAsk () {
      this.$modal.show('create-new-ask')
    },

    createASK () {
      if (!this.titleQuestion || !this.detailQuestion) return

      const data = {
        title: this.titleQuestion,
        body: this.detailQuestion,
        category_id: 1
      }

      request({
        url: URL.QUESTIONS,
        method: 'post',
        data: JSON.stringify(data)
      })
        .then(res => {
          this.$modal.hide('create-new-ask')
          EventBus.$emit('closeFormCreateASK')
          this.titleQuestion = ''
          this.detailQuestion = ''
        })
        .catch((e) => {
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
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

/* add ask */
.title-popup-ask {
  padding: 10px 20px;
  border-bottom: 1px solid #ccc;
}

.ask-user {
  display: flex;
}

.ask-user p{
  padding-top: 10px;
  font-size: 18px;
  color: #6c757d;
}

.ask-user img{
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 20px;
}

.popup-note {
  padding: 10px 20px;
  border-bottom: 1px solid #ccc;
}

.popup-note p {
  line-height: 0.5;
  font-size: 16px;
  font-weight: 500;
}

.ask-title {
  padding: 10px 20px;
  border-bottom: 1px solid #ccc;
}

.ask-title input {
  width: 100%;
  height: 50px;
  border: none;
  outline: none;
}

.ask-title input::placeholder {
  color: #bcb7b7;
  font-size: 20px;
  font-weight: 700;
}

.ask-deatail{
  width: 100%;
  border: none;
  outline: none;
  border-bottom: 1px solid #ccc;
}

.ask-deatail textarea{
  padding: 20px;
  width: 100%;
  border: none;
  outline: none;
}

.ask-deatail textarea::placeholder {
  color: #bcb7b7;
  font-size: 20px;
  font-weight: 700;
}

.action-ask {
  float: right;
  margin-right: 20px;
  padding-top: 10px;
}

.action-ask .action-cancel{
  border: none;
  background: none;
  margin-right: 20px;
  color: #6c757d;
  outline: none;
}

.action-ask .action-create{
  background-color: #708FDB;
  border: 1px solid #ccc;
  border-radius: 5px;
  color: white;
  padding: 5px 10px;
  font-weight: 700;
  outline: none;
}

</style>
