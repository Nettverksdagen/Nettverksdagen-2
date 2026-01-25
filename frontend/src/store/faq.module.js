const defaultState = {
  all: []
}

const state = {...defaultState}

const actions = {
  async fetchFAQs ({commit}) {
    commit('fetchRequest')

    try {
      const response = await fetch(process.env.VUE_APP_API_HOST + '/api/faq/')
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
  fetchSuccessful (state, faqs) {
    state.all = faqs
    state.loading = false
    state.loaded = true
  },
  fetchFailure () {
    console.log('Failed to fetch FAQs')
  },
  addFAQ (state, faq) {
    state.all.push(faq)
  },
  deleteFAQ (state, faq) {
    state.all = state.all.filter(f => f.id !== faq.id)
  },
  updateFAQ (state, faq) {
    const modify = state.all.findIndex(f => f.id === faq.id)
    state.all[modify] = faq
  }
}

export const faq = {
  namespaced: true,
  state,
  actions,
  getters,
  mutations
}