<template>
    <div class="qr-view">
        <Content>
            <b-form>
                <b-form-group id='input-name' :label-for="'input-name'"
                    description='Skriv inn navnet ditt:'>
                    <b-form-input id='input-name' v-model="form.name" required
                        placeholder='Navn'></b-form-input>
                </b-form-group>
                <b-form-group id='input-group-email' :label-for="'input-email'"
                    description='Skriv inn emailen din:'>
                    <b-form-input id='input-email' type="email" v-model="form.email" required
                        placeholder='E-post'></b-form-input>
                </b-form-group>
            </b-form>
            <div>
                <b-button variant='outline-secondary' @click="onCancel">
                    Avbryt
                </b-button>
                <b-button variant='primary' @click="onSubmit">
                    Registrer
                </b-button>
            </div>
        </Content>
    </div>
</template>

<script>
import Content from '@/components/common/Content.vue'
import axios from 'axios'
export default {
  name: 'QRRegistrationView',
  components: {
    Content
  },
  data () {
    return {
      form: {
        email: '',
        name: ''
      }
    }
  },
  computed: {
    sponsor () {
      return this.$route.params.id
    }
  },
  methods: {
    checkValidForm (check) {
      for (let key in check) {
        if (check[key] === '') {
          return false
        } else if (key === 'email') {
          let at = check[key].split('@')
          let dot = at[at.length - 1].split('.')
          if (at.length < 2 || dot.length < 2 || dot[dot.length - 1].length === 0) {
            return false
          }
        }
      }
      return true
    },
    onSubmit (e) {
      e.preventDefault()
      let data = this.$data.form
      // Generate and include 6-character random deregistering code
      if (this.checkValidForm(data)) {
        this.submitForm()
        // Clear data
        this.$data.show = false
        this.$data.form = {email: '', name: ''}
        this.$data.submitted = true
      }
    },
    submitForm () {
      console.log({id: this.$route.params.id, ...this.$data.form})
      axios.post(process.env.VUE_APP_API_HOST +
        '/api/spinthewheel/', {id: this.$route.params.id, ...this.$data.form})
        .then((response) => console.log(response))
        .catch((e) => {
          console.log('Error in submitForm')
          console.log(e)
        })
    },
    onCancel (e) {
      e.preventDefault()
      this.$data.form = {email: '', name: ''}
      this.$route.push({name: 'Home'})
    }
  }
}
</script>

<style lang="scss" scoped>
.qr-view {
    min-height: 80vh;
}
</style>
