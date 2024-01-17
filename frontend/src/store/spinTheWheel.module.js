const defaultState = {
  all: []
}

const state = {...defaultState}

const actions = {
  async fetchSpinTheWheel ({commit}) {
    commit('fetchRequest')
    try {
      const response = await fetch(process.env.VUE_APP_API_HOST + '/api/spinthewheel/')
      const all = await response.json()
      commit('fetchSuccessful', all)
    } catch (e) {
      commit('fetchFailure', e)
    }
  }
}

const getters = {}

const mutations = {
  fetchRequest (state) {
    state.loaded = false
    state.loading = true
  },
  fetchSuccessful (state, participants) {
    state.all = participants
    state.loading = false
    state.loaded = true
  },
  fetchFailure () {
    console.log('Failed to fetch spin the wheel data')
  },
  addTicket (state, ticket) {
    state.all.push(ticket)
  }
}

export const spinTheWheel = {
  namespaced: true,
  state,
  actions,
  getters,
  mutations
}
