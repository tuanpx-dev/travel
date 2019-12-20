<template>
  <div class="page-login">
    <div class="login container">
      <h1>TravelQA</h1>
      <div>
        <p
          class="login-title"
        >Welcome to TravelQA! To post or answer question, please register or login. <br/>Registration and use are free.</p>
        <div class="row login-content">
          <div class="col-md-6 col-xs-12">
            <div class="login-with-fa">
              <p>
                <i class="fa fa-facebook-square"></i>
              </p>
              <p>Login with facebook</p>
            </div>
            <div class="login-new-account">
              If tou are not a user,
              <a @click="showPopup">New Registration></a> By regisering as a new user, you are agreeing to the TravelQA's
              <a
                href=""
              >Term of Service</a> and
              <a href="">Privacy Policy</a>
            </div>
          </div>
          <div class="login-form col-md-6 col-xs-12">
            <p class="login-text">Login</p>
            <input type="text" placeholder="Email" class="login-value" />
            <input type="text" placeholder="Password" class="login-value" />
            <div class="action-login-resset">
              <button class="resset-password">Password Reset</button>
              <button class="action-login">Login</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <modal name="create-new-account">
      create-new-account
    </modal>
  </div>
</template>

<script>
import request from '../../request/request'
export default {
  name: 'Login',
  data () {
    return {
      loading: false
    }
  },

  created () {
    request({
      url: '/',
      method: 'get'
    }).then(res => {
      console.log('res', res)
    })
  },

  methods: {
    showPopup () {
      this.$modal.show('create-new-account')
    }
  }
}
</script>

<style lang="css" scoped>
.page-login {
  background-color: #B5D6F3;
  height: 100vh;
  padding: 4% 8%;
  display: flex;
    align-items: center;
}

.login {
  margin: 0 auto;
  background-color: white;
  border: 1px solid #ccc;
  color: black;
  width: 100%;
  height: auto;
}

.login h1 {
  font-size: 100px;
}

.login-new-account {
  text-align: left;
  margin-top: 10px;
  font-size: 25px;
  color: gray;
  font-weight: 400;
}

.login-with-fa {
  background: #4267b2;
  color: white;
  font-size: 30px;
  font-weight: 600;
  height: 55px;
  display: flex;
  justify-content: space-around;
  padding-top: 8px;
  margin-bottom: 20px;
}

.login-title {
  font-size: 25px;
  text-align: left;
  margin-top: 5%;
}

.login-text {
  font-size: 24px;
  font-weight: bold;
}

.login-value {
  margin-bottom: 10px;
  height: 50px;
  padding-left: 10px;
  background-color: #ccc;
  border: 1px solid #6c757d;
}

.login-content {
  display: flex;
  flex-wrap: wrap;
}

.login-form {
  border-left: 1px solid gray;
  display: flex;
  flex-direction: column;
  text-align: left;
  font-size: 25px;
}

.action-login-resset {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.resset-password {
  border: none;
  background: none;
  outline: none;
}

.action-login {
  background-color: #4267b2;
  border: 1px solid #4267b2;
  padding: 0 10px;
  border-radius: 5px;
  color: white;
  font-weight: bold;
  outline: none;
}

@media only screen and (max-width: 600px) {
  .login {
    padding: 20px;
  }

  .login h1 {
    font-size: 50px;
  }

  .login-title {
    font-size: 16px;
    text-align: left;
    margin-top: 5%;
  }

  .login-with-fa {
    font-size: 16px;
    height: 40px;
  }

  .login-new-account {
    font-size: 16px;
  }

  .login-form {
    font-size: 16px;
  }

  .login-text {
    font-size: 18px;
  }

  .login-value {
    height: 35px;
  }

  .fa-facebook-square {
    font-size: 24px;
  }

  .login-form {
    border: none;
  }
}

@media only screen and (min-width: 768px) {
  .login {
    padding: 20px;
  }

  .login-title {
    font-size: 16px;
    text-align: left;
    margin-top: 5%;
  }

  .login-with-fa {
    font-size: 16px;
    height: 40px;
  }

  .login-new-account {
    font-size: 16px;
  }

  .login-form {
    font-size: 16px;
  }

  .login-value {
    height: 40px;
  }
  .fa-facebook-square {
    font-size: 24px;
  }
}

@media only screen and (min-width: 1024px) {
  .login {
    padding: 20px;
    padding: 5% 15%;
  }

  .fa-facebook-square {
    font-size: 24px;
  }
}
</style>
