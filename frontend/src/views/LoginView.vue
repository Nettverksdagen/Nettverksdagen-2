<template>
  <div class="login-view">
    <b-row align-v="center main-container">
      <b-col>
        <b-row align-h="center">
          <b-col cols="12" sm="10" md="7" lg="6" xl="4">
            <b-row class="login-container">
              <b-col cols="7" class="d-none d-sm-block text-container">
                <div class="padder">
                  <h1>Logg inn</h1>
                  <span>Det er på tide at noe blir gjort her</span>
                  <hr>
                  <span class="subtitle faded">Har du ikke bruker? Kontakt IT.</span>
                </div>
              </b-col>
              <b-col cols="12" sm="5" class="form-container">
                <div class="padder">
                  <b-form-input class="my-2" type="text" placeholder="Brukernavn"></b-form-input>
                  <b-form-input class="my-2 mb-4" type="password" placeholder="Passord"></b-form-input>
                  <b-button size="lg" variant="success" class="mb-1 login-button">Logg inn</b-button>
                  <b-link class="forgot-password-link" href="#">Glemt passord?</b-link>
                </div>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  name: 'LoginView'
}
</script>

<style scoped lang="scss">
  $form-color: #28a771;
  .login-view {
    min-width:100vh;
    min-height:100vh;
    background: url('../assets/login_bg.jpg') no-repeat center;
    background-size: cover;
    .main-container {
      min-height:100vh;
    }
    .login-container {
      box-shadow:0 2px 10px rgba(0,0,0,0.15);
      overflow: hidden;
      border-radius:5px;
    }
    .text-container {
      background: $form-color;
      color:#fff;
      h1 {
        font-weight:600;
        margin:0;
        padding:0;
      }
      .subtitle {
        font-weight:lighter;
        font-size:15px;
        &.faded {
          opacity:0.8;
        }
      }
    }
    .form-container {
      background:#fff;
    }
    .padder {
      margin-top:100px;
      margin-bottom:60px;
    }
    .login-button {
      width:100%;
      background-color:$form-color;
      border-color:$form-color;
    }
    .forgot-password-link {
      color:#999;
      font-size:15px;
    }
  }
</style>
