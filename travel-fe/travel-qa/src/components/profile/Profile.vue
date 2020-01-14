<template>
  <div class="profile">
    <div class="desktop-profile">

    </div>

    <div class="mobile-profile">
      <div class="avartar-name">
        <img src="https://scontent.fhan2-4.fna.fbcdn.net/v/l/t1.0-9/79718560_558443374887450_3199243511551492096_n.jpg?_nc_cat=100&_nc_ohc=wwxTklQV7QgAQkI9nPX_W92osAYeK6NMO3Sk0yYTImrPEDpKoETFGrQQg&_nc_ht=scontent.fhan2-4.fna&oh=4484df51e86cb97abeb83d0f70910f0e&oe=5E781D35" alt="">
        <p>name</p>
      </div>
      <div class="border-content-profile"></div>

      <div class="note-des">
        xxxxx
      </div>
      <div class="border-content-profile"></div>

      <div class="review-user">
        <p class="title-section">Account setting</p>
        <div>
          <div class="change-review">
            <p class="change-title title-section">Name</p>
            <p v-if="true" class="change-value title-section">{{user.username}}</p>
            <input v-else type="text">
            <p class="icon-edit-review title-section"><i class="fa fa-pencil" style="color: #2761E6"></i></p>
          </div>
          <div class="change-review">
            <p class="change-title title-section">Age</p>
            <p v-if="true" class="change-value title-section">{{user.age}}</p>
            <input v-else type="text">
            <p class="icon-edit-review title-section"><i class="fa fa-pencil" style="color: #2761E6"></i></p>
          </div>
          <div class="change-review">
            <p class="change-title title-section">E-mail</p>
            <p v-if="true" class="change-value title-section">{{user.email}}</p>
            <input v-else type="text">
            <p class="icon-edit-review title-section"><i class="fa fa-pencil" style="color: #2761E6"></i></p>
          </div>
          <div class="change-review">
            <p class="change-title title-section">Password</p>
            <p v-if="true" class="change-value title-section change-password">Change the password</p>
            <input v-else type="text">
          </div>
        </div>
      </div>
      <div class="border-content-profile"></div>

      <div class="interest">
        <p>Interest</p>
        <Category />
      </div>
    </div>
  </div>
</template>

<script>
import Category from '../ask/Filter'
export default {
  name: 'Profile',
  components: {
    Category
  },

  data () {
    return {
      user: {}
    }
  },

  created () {
    this.user = JSON.parse(localStorage.getItem('user')).data.user
  },

  methods: {

  }
}
</script>

<style lang="css" scoped>
.profile {
  width: 50%;
  margin: 0 auto;
  text-align: left
}

.desktop-profile {

}

.mobile-profile {
  display: none;
}

.avartar-name {
  display: flex;
  padding-left: 10px
}

.avartar-name img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.avartar-name p {
  font-size: 20px;
  padding-left: 10px;
  padding-top: 10px;
}

.note-des {
  padding-left: 10px;
  font-size: 14px;
  height: 70px;
  max-height: 100px;
}

.review-user {
  padding-left: 10px;
  font-size: 14px;
}

.change-review {
  display: flex;
  padding: 5px 10px 0 10px;
  border-bottom: 1px solid #CBE0FF;
}

.change-title {
  width: 35%;
}

.change-value {
  width: 60%;
}

.change-password {
  color: #2761E6;
}

.border-content-profile {
  border-top: 1px solid #2761E6;
  height: 5px;
  background-color: #CBE0FF;
  margin-bottom: 5px;
}

.title-section {
  padding: 0;
  margin: 0;
}

.interest {
  padding-left: 10px;
}

@media only screen and (max-width: 600px) {
  .profile {
    width: 100%;
  }

  .desktop-profile {
    display: none;
  }

  .mobile-profile {
    display: block;
  }
}
</style>
