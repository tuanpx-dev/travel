<template>
  <div class="row header">
    <div class="col-md-3 col-xs-10 header-title-app">
      <div>
        <p class="logo" @click="backToHome">TravelQA</p>
        <button class="button-ask" @click="addAsk()">Ask</button>
      </div>
    </div>
    <div class="user" v-if="isShowAvatar">
      <img v-if='user.img' :src="user.img" alt="" class="avatar-user">
      <img
        v-else
        class="avatar-user"
        src="https://scontent.fhan2-4.fna.fbcdn.net/v/l/t1.0-9/79718560_558443374887450_3199243511551492096_n.jpg?_nc_cat=100&_nc_ohc=wwxTklQV7QgAQkI9nPX_W92osAYeK6NMO3Sk0yYTImrPEDpKoETFGrQQg&_nc_ht=scontent.fhan2-4.fna&oh=4484df51e86cb97abeb83d0f70910f0e&oe=5E781D35"
        alt=""
        @click="nextToProfile"
      >
    </div>

    <div class="user-mobile" v-if="isShowAvatar">
      <img v-if='user.img' :src="user.img" alt="" class="avatar-user">
      <img
        v-else
        class="avatar-user"
        src="https://scontent.fhan2-4.fna.fbcdn.net/v/l/t1.0-9/79718560_558443374887450_3199243511551492096_n.jpg?_nc_cat=100&_nc_ohc=wwxTklQV7QgAQkI9nPX_W92osAYeK6NMO3Sk0yYTImrPEDpKoETFGrQQg&_nc_ht=scontent.fhan2-4.fna&oh=4484df51e86cb97abeb83d0f70910f0e&oe=5E781D35"
        alt=""
        @click="showModalProfile"
      >
    </div>

    <Ask
      :name="namePopup"
      :width="'60%'"
      @closeASK="closeASK"
    />

    <Ask
      :name="'create-ask-mobile'"
      :width="'90%'"
      @closeASK="closeASKMobile"
    />

    <modal
      name="avatar-profile"
      :pivotX="1"
      :pivotY="0"
      width="50%"
      height="auto"
      :scrollable="true">

      <div class="popup-profile-avarta">
        <img v-if='user.img' :src="user.img" alt="">
        <img
          v-else
          src="https://scontent.fhan2-4.fna.fbcdn.net/v/l/t1.0-9/79718560_558443374887450_3199243511551492096_n.jpg?_nc_cat=100&_nc_ohc=wwxTklQV7QgAQkI9nPX_W92osAYeK6NMO3Sk0yYTImrPEDpKoETFGrQQg&_nc_ht=scontent.fhan2-4.fna&oh=4484df51e86cb97abeb83d0f70910f0e&oe=5E781D35"
          alt=""
        >
        <p>{{user.username}}</p>
      </div>

      <div class="ask-popup-profile">
        <button @click="addAskMobile()">Ask</button>
      </div>
      <div class="popup-profile-border"></div>

      <div class="menu-profile">
        <p>Post</p>
        <div>
          <p @click="nextToMyQuestion">My question</p>
          <p @click="nextToMyAnswer">My answer</p>
        </div>
      </div>
      <div class="popup-profile-border"></div>

      <div class="list-category-profile">
        <p>Category</p>
        <p class="category-item-profile" v-for="(category, index) in categorys" :key="index">{{category.name}}</p>
      </div>
      <div class="action-profile-popup">
        <div @click="nextToProfile">Profile</div>
        <div>Logout</div>
      </div>
    </modal>
  </div>
</template>

<script>
import Ask from '../ask/ask'
import request from '../../../request/request'
import { URL } from '../../api/URL'

export default {
  name: 'Header',
  components: {
    Ask
  },

  data () {
    return {
      namePopup: 'create-ask',
      titleQuestion: '',
      detailQuestion: '',
      user: {},
      isShowAvatar: true,
      categorys: []
    }
  },

  created () {
    this.getCategory()
    this.user = JSON.parse(localStorage.getItem('user')).data.user
    if (this.$router.currentRoute.name === 'ProfileUser') {
      this.isShowAvatar = false
    }
  },

  methods: {
    nextToMyQuestion () {
      this.$router.push({ path: '/myQuestion' })
      this.$modal.hide('avatar-profile')
    },

    nextToMyAnswer () {
      this.$router.push({ path: '/myAnswers' })
      this.$modal.hide('avatar-profile')
    },

    showModalProfile () {
      this.$modal.show('avatar-profile')
    },

    backToHome () {
      this.$router.push({ path: '/' })
    },

    closeASK () {
      this.$modal.hide(this.namePopup)
    },

    closeASKMobile () {
      this.$modal.hide('create-ask-mobile')
    },

    addAsk () {
      this.$modal.show(this.namePopup)
    },

    addAskMobile () {
      this.$modal.hide('avatar-profile')
      this.$modal.show('create-ask-mobile')
    },

    nextToProfile () {
      this.$router.push({ path: '/profile' })
      this.$modal.hide('avatar-profile')
    },

    getCategory () {
      request({
        url: URL.CATEGORY,
        method: 'get'
      })
        .then(res => {
          this.categorys = res.data
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
  padding-top: 20px;
  justify-content: space-between;
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
/* user */
.user {
  display: block;
}

.user-mobile {
  display: none;
}

.avatar-user {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  float: right;
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

@media only screen and (max-width: 600px) {
  .button-ask {
    display: none;
  }

  .user {
    display: none;
  }

  .header {
    background-color: #2761E6;
    padding: 0;
    margin-bottom: 10px;
  }

  .logo {
    color: white;
    border: none;
    padding: 10px;
    font-size: 30px;
    font-weight: 700;
  }

  .header .col-md-3{
    z-index: 0;
  }

  .header-title-app {
    position: relative;
  }

  .user-mobile {
    display: block;
    position: absolute;
    right: 5px;
    top: 8px;
  }

  .popup-profile-avarta {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px;
    text-align: center;
    background-color: #2761E6;
    color: white;
  }

  .popup-profile-avarta img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 20px;
  }
  .popup-profile-avarta p {
    padding-top: 10px;
    font-weight: 700;
  }

  .ask-popup-profile {
    text-align: center;
  }

  .ask-popup-profile button {
    padding: 5px 20px;
    background-color: #2761E6;
    margin: 10px 0;
    color: white;
    border: 1px;
    border-radius: 10px;
    outline: none;
  }

  .popup-profile-border {
    border-top: 1px solid #2761E6;
    height: 5px;
    background-color: #CBE0FF;
  }

  .menu-profile {
    line-height: 1;
    padding-left: 10px;
  }

  .menu-profile div {
    padding-left: 10px;
  }

  .list-category-profile {
    padding-left: 10px;
    line-height: 1;
  }

  .category-item-profile {
    padding-left: 10px;
  }

  .action-profile-popup {
    background-color: #CBE0FF;
    padding: 10px;
  }
}
</style>
