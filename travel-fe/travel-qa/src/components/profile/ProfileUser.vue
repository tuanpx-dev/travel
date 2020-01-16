<template>

    <div class="col-md-9">
      <div class="avartar-name mobile-profile">
        <img
          src="https://scontent.fhan2-4.fna.fbcdn.net/v/l/t1.0-9/79718560_558443374887450_3199243511551492096_n.jpg?_nc_cat=100&_nc_ohc=wwxTklQV7QgAQkI9nPX_W92osAYeK6NMO3Sk0yYTImrPEDpKoETFGrQQg&_nc_ht=scontent.fhan2-4.fna&oh=4484df51e86cb97abeb83d0f70910f0e&oe=5E781D35"
          alt
        />
        <p>name</p>
      </div>
      <div class="border-content-profile mobile-profile"></div>

      <div class="note-des">xxxxx</div>
      <div class="border-content-profile-destop"></div>
      <div class="border-content-profile mobile-profile"></div>

      <div class="review-user">
        <p class="title-section">Account setting</p>
        <div>
          <div class="change-review-desktop">
            <p class="change-title title-section">Name</p>
            <p v-if="true" class="change-value title-section">{{user.username}}</p>
            <input v-else type="text" />
            <p class="icon-edit-review title-section">
              <i class="fa fa-pen" style="color: #2761E6"></i>
            </p>
          </div>
          <div class="change-review-desktop">
            <p class="change-title title-section">Age</p>
            <p v-if="true" class="change-value title-section">{{user.age}}</p>
            <input v-else type="text" />
            <p class="icon-edit-review title-section">
              <i class="fa fa-pen" style="color: #2761E6"></i>
            </p>
          </div>
          <div class="change-review-desktop">
            <p class="change-title title-section">E-mail</p>
            <p v-if="true" class="change-value title-section">{{user.email}}</p>
            <input v-else type="text" />
            <p class="icon-edit-review title-section">
              <i class="fa fa-pen" style="color: #2761E6"></i>
            </p>
          </div>
          <div class="change-review-desktop">
            <p class="change-title title-section">Password</p>
            <p v-if="true" class="change-value title-section change-password">Change the password</p>
            <input v-else type="text" />
          </div>
        </div>
      </div>
      <div class="border-content-profile-destop"></div>
      <div class="border-content-profile mobile-profile"></div>

      <div class="interest">
        <p>Interest</p>
        <Category />
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

  methods: {}
}
</script>

<style lang="css" scoped>
.profile {
  width: 80%;
  margin: 0 auto;
  text-align: left;
  padding-left: 100px;
}

.desktop-profile {
}

.profile-username {
  border-bottom: 1px solid #ccc;
  margin-bottom: 10px;
  display: flex;
  padding-bottom: 10px;
  margin-top: -15px;
}

.profile-username img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-right: 10px;
}

.follow {
  margin-top: 30px;
}

.sidebar-profile {
  border: 1px solid black;
  min-height: 300px;
  padding: 10px;
  display: flex;
  flex-direction: column;
}

.active-profile {
  border-radius: 10px;
  background-color: #ccc;
}

.sidebar-profile-action {
  border: none;
  text-align: left;
  padding: 10px;
  margin-bottom: 5px;
}

.mobile-profile {
  display: none;
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
  border-bottom: 1px solid #cbe0ff;
}

.change-review-desktop {
  display: flex;
  padding: 5px 10px 0 10px;
  border-bottom: 1px solid #ccc;
  margin-bottom: 3px;
}

.change-review-desktop:last-child {
  border-bottom: none;
}

.change-title {
  width: 35%;
}

.change-value {
  width: 60%;
}

.change-password {
  color: #2761e6;
}

.border-content-profile {
  border-top: 1px solid #2761e6;
  height: 5px;
  background-color: #cbe0ff;
  margin-bottom: 5px;
}

.border-content-profile-destop {
  border-bottom: 1px solid #ccc;
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
    padding: 0;
  }

  .desktop-profile {
    display: none;
  }

  .mobile-profile {
    display: block;
  }

  .avartar-name {
    display: flex;
    padding-left: 10px;
  }
}
</style>
