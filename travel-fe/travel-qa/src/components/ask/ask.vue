<template>
    <modal
      :name="name"
      width="60%"
      maxHeight="600px"
      :reset="true"
      :scrollable="true"
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
        <button class="action-cancel" @click="$emit('closeASK')">Cancel</button>
        <button class="action-create" @click="createASK">Question</button>
      </div>
    </modal>
</template>

<script>
import { EventBus } from '../../eventBus'
import request from '../../../request/request'
import { URL } from '../../api/URL'

export default {
  name: 'Ask',
  props: ['question', 'name'],

  data () {
    return {
      titleQuestion: '',
      detailQuestion: '',
      user: {}
    }
  },

  created () {
    this.$modal.show(this.name)
    if (this.question) {
      this.titleQuestion = this.question.title
      this.detailQuestion = this.question.body
    }

    this.user = JSON.parse(localStorage.getItem('user')).data.user
  },

  methods: {
    createASK () {
      if (!this.titleQuestion || !this.detailQuestion) return

      if (this.question) {
        // todo
      }

      const data = {
        title: this.titleQuestion,
        body: this.detailQuestion,
        category_id: 1
      }

      request({
        url: URL.CREATE_QUESTION,
        method: 'post',
        data: JSON.stringify(data)
      })
        .then(res => {
          this.$modal.hide(this.name)
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
