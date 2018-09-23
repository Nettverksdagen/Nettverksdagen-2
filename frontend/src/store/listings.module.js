const defaultState = {
  all: []
}

const state = {...defaultState}

const actions = {
  async fetchListings ({commit}) {
    commit('fetchRequest')

    try {
      const response = await fetch('http://127.0.0.1:8000/api/listing/')
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
  fetchSuccessful (state, listings) {
    state.all = listings
    state.loading = false
    state.loaded = true
  },
  fetchFailure () {
    console.log('Failed to fetch listings')
  }
}

export const listings = {
  namespaced: true,
  state,
  actions,
  getters,
  mutations
}
