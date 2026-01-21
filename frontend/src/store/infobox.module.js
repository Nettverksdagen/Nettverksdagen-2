const defaultState = {
  title: null,
  paragraph: null,
}

const state = {...defaultState}

const actions = {
  async fetchInfobox ({commit}) {
    commit('fetchRequest')
   
    try {
      const response = await fetch(process.env.VUE_APP_API_HOST + '/api/infobox/')
      const all = await response.json()
      commit('fetchSuccessful', all[0])
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
  fetchSuccessful (state, data) {
    state.title = data.title
    state.paragraph = data.paragraph
    state.loading = false
    state.loaded = true
  },
  fetchFailure () {
    console.log('Failed to fetch infobox')
  },
}

export const infobox = {
  namespaced: true,
  state,
  actions,
  getters,
  mutations
}
