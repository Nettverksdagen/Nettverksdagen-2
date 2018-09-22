const defaultState = {
  listings: []

}

const state = {...defaultState}

const actions = {
  async fetchListings ({commit}) {
    commit('fetchRequest')

    try {
      const response = await fetch('http://127.0.0.1:8000/api/listing/')
      const listings = await response.json()
      commit('fetchSuccessful', listings)
    } catch (e) {
      commit('fetchFailure', e)
    }
  }
}

const getters = {
  all (state) {
    return state.listings
  }
}

const mutations = {
  fetchRequest (state) {
    state.loaded = false
    state.loading = true
  },
  fetchSuccessful (state, listings) {
    state.listings = listings
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
