<template>
  <div class="profile">
    <div class="">
      <div class="profile-username desktop-profile">
        <img src="https://scontent.fhan2-4.fna.fbcdn.net/v/l/t1.0-9/79718560_558443374887450_3199243511551492096_n.jpg?_nc_cat=100&_nc_ohc=wwxTklQV7QgAQkI9nPX_W92osAYeK6NMO3Sk0yYTImrPEDpKoETFGrQQg&_nc_ht=scontent.fhan2-4.fna&oh=4484df51e86cb97abeb83d0f70910f0e&oe=5E781D35" alt="">
        <div>
          <div class="user-profile-deatail">
            <h3>{{user.username}}</h3>
            <p>{{user.age}} &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; Enter Residential Area</p>
            <p>Enter Self-Introduction</p>
          </div>
          <div class="follow">24 followers</div>
        </div>
      </div>

      <div class="row">
        <div class="sidebar-profile col-md-3 desktop-profile">
          <button class="sidebar-profile-action" @click="nextToProfileUser" :class="{ 'active-profile': activeSidebar === 1 }">Profile</button>
          <button class="sidebar-profile-action" @click="nextToMyQuestion" :class="{ 'active-profile': activeSidebar === 2 }">Question</button>
          <button class="sidebar-profile-action" @click="nextToMyAnswer" :class="{ 'active-profile': activeSidebar === 3 }">Answers</button>
        </div>

        <router-view></router-view>
      </div>

    </div>
  </div>
</template>

<script>
import Category from '../ask/Filter'
import ProfileUser from './ProfileUser'

export default {
  name: 'Profile',
  components: {
    Category,
    ProfileUser
  },

  data () {
    return {
      user: {},
      activeSidebar: 1
    }
  },

  created () {
    this.user = JSON.parse(localStorage.getItem('user')).data.user

    if (this.$router.currentRoute.name === 'ProfileUser') {
      this.activeSidebar = 1
    } else if (this.$router.currentRoute.name === 'MyQuestion') {
      this.activeSidebar = 2
    } else {
      this.activeSidebar = 3
    }
  },

  methods: {
    nextToMyQuestion () {
      this.$router.push({ path: '/myQuestion' })
      this.activeSidebar = 2
    },

    nextToProfileUser () {
      this.$router.push({ path: '/profile' })
      this.activeSidebar = 1
    },

    nextToMyAnswer () {
      this.$router.push({ path: '/myAnswers' })
      this.activeSidebar = 3
    }
  }
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
  height: 400px;
  max-height: 500px;
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
  outline: none;
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
  border-bottom: 1px solid #CBE0FF;
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
  color: #2761E6;
}

.border-content-profile {
  border-top: 1px solid #2761E6;
  height: 5px;
  background-color: #CBE0FF;
  margin-bottom: 5px;
}

.border-content-profile-destop {
  border-bottom: 1px solid #ccc
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
    padding-left: 10px
  }
}
</style>
