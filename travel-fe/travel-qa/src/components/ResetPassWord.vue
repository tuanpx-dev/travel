<template>
  <div class="page-login">
    <div class="login">
        <h1>TravelQA</h1>
        <div>
        </div>
    </div>
  </div>
</template>

<script>
import request from '../../request/request'
export default {
  name: 'ResetPassWord',
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
  }
}
</script>

<style lang="css" scoped>
.page-login {
  background-color: #B5D6F3;
  height: 100vh;
  padding: 4% 8%;
}

.login {
  margin: 0 auto;
  background-color: white;
  border: 1px solid #ccc;
  color: black;
  width: 100%;
  height: 100%;
}

.login h1 {
  font-size: 100px;
}

@media only screen and (max-width: 600px) {
  .login {
    padding: 20px;
  }

  .login h1 {
    font-size: 50px;
  }
}

@media only screen and (min-width: 768px) {
  .login {
    padding: 20px;
  }
}

@media only screen and (min-width: 1024px) {
  .login {
    padding: 20px;
    padding: 5% 15%;
  }
}
</style>
