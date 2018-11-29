const defaultState = {
  all: []
}

const state = {...defaultState}

const actions = {
  async fetchBusinesses ({commit}) {
    commit('fetchRequest')

    try {
      const response = await fetch('http://127.0.0.1:8000/api/business/')
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
  fetchSuccessful (state, businesses) {
    state.all = businesses
    state.loading = false
    state.loaded = true
  },
  fetchFailure () {
    console.log('Failed to fetch businesses')
  },
  addBusiness (state, business) {
    state.all.push(business)
  }
}

export const businesses = {
  namespaced: true,
  state,
  actions,
  getters,
  mutations
}
