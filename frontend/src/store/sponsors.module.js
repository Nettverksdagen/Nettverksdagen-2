const defaultState = {
  all: []
}

const state = {...defaultState}

const actions = {
  async fetchSponsors ({commit}) {
    commit('fetchRequest')

    try {
      const response = await fetch('http://127.0.0.1:8000/api/sponsor/')
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
  fetchSuccessful (state, sponsors) {
    state.all = sponsors
    state.loading = false
    state.loaded = true
  },
  fetchFailure () {
    console.log('Failed to fetch sponsors')
  },
  addSponsor (state, sponsor) {
    state.all.push(sponsor)
  }
}

export const sponsors = {
  namespaced: true,
  state,
  actions,
  getters,
  mutations
}
