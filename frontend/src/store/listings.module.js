const defaultState = {
  all: []
}

const state = {...defaultState}

const actions = {
  async fetchListings ({commit}) {
    commit('fetchRequest')

    try {
      const response = await fetch(process.env.VUE_APP_API_HOST + '/api/listing/')
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
  },
  addListing (state, listing) {
    state.all.push(listing)
  },
  deleteListing (state, listing) {
    state.all = state.all.filter(lst => lst.id !== listing.id)
  },
  updateListing (state, listing) {
    const modify = state.all.findIndex(lst => lst.id === listing.id)
    state.all[modify] = listing
  }
}

export const listings = {
  namespaced: true,
  state,
  actions,
  getters,
  mutations
}
