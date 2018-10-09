const defaultState = {
  username: '',
  token: ''
}

const state = {...defaultState}

const actions = {
  async login ({commit}, credentialObserver) {
    commit('loggingIn')

    let credentials = credentialObserver.credentials // Get credentials from observer

    fetch('http://127.0.0.1:8000/rest-auth/login/', {
      method: 'POST',
      body: JSON.stringify({
        username: credentials.username,
        password: credentials.password
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(response => response.json())
      .then(function (response) {
        if (response.hasOwnProperty('key')) {
          console.log(response.key)
          commit('loggedInSuccessfully', {
            username: credentials.username,
            token: response.key
          })
        } else if (response.hasOwnProperty('non_field_errors')) {
          commit('loginFailure')
        } else {
          commit('fetchFailure')
        }
      })
      .catch(error => commit('fetchFailure', error))
  }
}

const getters = {}

const mutations = {
  loggingIn (state) {
    state.loggingIn = true
  },
  loggedInSuccessfully (state, payload) {
    state.username = payload.username
    state.token = payload.token
    state.loggingIn = false
  },
  loginFailure () {
    console.log('Wrong login credentials')
    state.loggingIn = false
  },
  fetchFailure (error) {
    console.log('Could not log in because of an error: ', error)
    state.loggingIn = false
  }
}

export const admin = {
  namespaced: true,
  state,
  actions,
  getters,
  mutations
}
