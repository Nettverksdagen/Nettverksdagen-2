const defaultState = {
  username: '',
  token: '',
  loggedIn: false
}

const state = {...defaultState}

const actions = {
  async login ({commit}, credentialObserver) {
    commit('loggingIn')

    let credentials = credentialObserver.credentials // Get credentials from observer

    await fetch(process.env.VUE_APP_API_HOST + '/rest-auth/login/', {
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
          commit('loggedInSuccessfully', {
            username: credentials.username,
            token: response.key,
            loggedIn: true
          })
        } else if (response.hasOwnProperty('non_field_errors')) {
          commit('loginFailure')
        } else {
          commit('fetchFailure')
        }
      })
      .catch(error => commit('fetchFailure', error))
  },
  async logout({commit}){
    commit('loggingOut')

    commit('loggedOutSuccessfully', {
      username: '',
      token: '',
      loggedIn: false
    })
    console.log("Logged out");
  } 
}

const getters = {}

const mutations = {
  loggingIn (state) {
    state.loggingIn = true
  },
  loggingOut (state) {
    state.loggingOut = true
  },
  loggedInSuccessfully (state, payload) {
    state.username = payload.username
    state.token = payload.token
    state.loggingIn = false
    state.loggedIn = true
  },
  loggedOutSuccessfully (state, payload) {
    state.username = ''
    state.token = ''
    state.loggingOut = false
    state.loggedIn = false
  },
  loginFailure () {
    console.log('Wrong login credentials')
    state.loggingIn = false
    state.loggedIn = false
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
