<template>

    <div class="col-md-9">
      <div class="avartar-name mobile-profile">
        <img
          :src="user.avarta"
          alt
        />
        <p>{{user.username}}</p>
      </div>
      <div class="border-content-profile mobile-profile"></div>

      <div class="note-des">{{user.place}}</div>
      <div class="border-content-profile-destop"></div>
      <div class="border-content-profile mobile-profile"></div>

      <div class="review-user">
        <p class="title-section">Account setting</p>
        <div>
          <div class="change-review-desktop">
            <p class="change-title title-section">Residence</p>
            <p v-if="!isEditName" class="change-value title-section">{{user.username}}</p>
            <input v-else type="text" v-model="username" class="input-edit"/>
            <p class="icon-edit-review title-section">
              <i v-if="!isEditName" class="fa fa-pen" style="color: #2761E6" @click="edit('name')"></i>
              <i v-else class="fas fa-check" style="color: green;" @click="editDone('name')"></i>
            </p>
          </div>
          <div class="change-review-desktop">
            <p class="change-title title-section">Age</p>
            <p v-if="!isEditAge" class="change-value title-section">{{user.age}}</p>
            <input v-else type="text" v-model="age" class="input-edit"/>
            <p class="icon-edit-review title-section">
              <i v-if="!isEditAge" class="fa fa-pen" style="color: #2761E6" @click="edit('age')"></i>
              <i v-else class="fas fa-check" style="color: green;" @click="editDone('age')"></i>
            </p>
          </div>
          <div class="change-review-desktop">
            <p class="change-title title-section">E-mail</p>
            <p v-if="!isEditEmail" class="change-value title-section">{{user.email}}</p>
            <input v-else type="text" v-model="email" class="input-edit"/>
            <p class="icon-edit-review title-section">
              <i v-if="!isEditEmail" class="fa fa-pen" style="color: #2761E6" @click="edit('email')"></i>
              <i v-else class="fas fa-check" style="color: green;" @click="editDone('email')"></i>
            </p>
          </div>
          <div class="change-review-desktop">
            <p class="change-title title-section">Password</p>
            <p v-if="!isEditPass" class="change-value title-section change-password" @click="edit('pass')">Change the password</p>
            <div v-else >
              <div>
                <input type="text" v-model="oldPass" class="input-edit"/>
                <input type="text" v-model="newPass" class="input-edit"/>
              </div>
              <p v-if="errorPass" style="color: red;">The password is incorrect! </p>
              <div>
                <button class="cancel-save-pass" @click="cancelPass">Cancel</button>
                <button class="button-save-pass" @click="editPass">Save</button>
              </div>
            </div>
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
import request from '../../../request/request'
import {URL} from '../../api/URL'

export default {
  name: 'Profile',
  components: {
    Category
  },

  data () {
    return {
      user: {},
      isEditName: false,
      isEditAge: false,
      isEditEmail: false,
      isEditPass: false,
      errorPass: false,

      username: '',
      age: '',
      email: '',
      oldPass: '',
      newPass: ''
    }
  },

  created () {
    this.user = JSON.parse(localStorage.getItem('user')).data.user
  },

  methods: {
    edit (edit) {
      switch (edit) {
        case 'name':
          this.isEditName = true
          this.username = this.user.username
          // this.editProfile(edit)
          break
        case 'age':
          this.isEditAge = true
          this.age = this.user.age
          // this.editProfile(edit)
          break
        case 'email':
          this.isEditEmail = true
          this.email = this.user.email
          // this.editProfile(edit)
          break
        case 'pass':
          this.isEditPass = true
          break
        default:
          break
      }
    },

    editDone (key) {
      let data = {
        display_name: this.user.username,
        email: this.user.email,
        age: this.user.age,
        place: '',
        avatar: this.user.avatar
      }

      switch (key) {
        case 'name':
          this.isEditName = false
          data.display_name = this.username
          break
        case 'age':
          this.isEditAge = false
          data.age = this.age
          break
        case 'email':
          this.isEditEmail = false
          data.email = this.email
          break
        default:
          break
      }

      request({
        url: URL.EDIR_USER,
        method: 'put',
        data: JSON.stringify(data)
      })
        .then(res => {

        })
        .catch((e) => {
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    editPass () {
      let data = {
        old_password: this.oldPass,
        new_password: this.newPass
      }

      request({
        url: URL.EDIT_PASS,
        method: 'put',
        data: JSON.stringify(data)
      })
        .then(res => {
          this.isEditPass = false
        })
        .catch((e) => {
          this.errorPass = true
          if (e.response.status === 401) {
            localStorage.setItem('user', null)
            this.$router.push({ path: '/login' })
          }
        })
    },

    cancelPass () {
      this.isEditPass = false
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

.input-edit {
  width: 55%;
  border: 1px solid #ccc;
  padding-left: 5px;
  border-radius: 5px;
  margin-right: 15px;
  margin-bottom: 3px;
}

.button-save-pass {
  background-color: green;
  padding: 0 10px;
  border-radius: 5px;
  border: 1px;
  outline: none;
  color: white;
}

.cancel-save-pass {
    border-radius: 5px;
    background-color: red;
    color: white;
    padding: 0 10px
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
