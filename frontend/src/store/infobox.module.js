const defaultState = {
  title_nb: null,
  title_en: null,
  paragraph_nb: null,
  paragraph_en: null,
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
    state.title_nb = data.title_nb
    state.title_en = data.title_en
    state.paragraph_nb = data.paragraph_nb
    state.paragraph_en = data.paragraph_en
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
