const defaultState = {
  all: []
}

const state = {...defaultState}

const actions = {
  async fetchForms ({commit}) {
    commit('fetchRequest')

    try {
      const response = await fetch(process.env.VUE_APP_API_HOST + '/api/form/')
      const all = await response.json()
      commit('fetchSuccessful', all)
    } catch (e) {
      commit('fetchFailure', e)
    }
  }
}

const getters = {
  // Get a form by the form's internal url
  form: (state) => (internalUrl) => {
    console.log(internalUrl)
    for (let i = 0; i < state.all.length; i++) {
      if (state.all[i].internal_url === internalUrl) {
        return state.all[i]
      }
    }
    return null
  }
}

const mutations = {
  fetchRequest (state) {
    state.loaded = false
    state.loading = true
  },
  fetchSuccessful (state, forms) {
    state.all = forms
    state.loading = false
    state.loaded = true
  },
  fetchFailure () {
    console.log('Failed to fetch forms')
  },
  addForm (state, form) {
    state.all.push(form)
  },
  deleteForm (state, form) {
    state.all = state.all.filter(frm => frm.id !== form.id)
  },
  updateForm (state, form) {
    const modify = state.all.findIndex(frm => frm.id === form.id)
    state.all[modify] = form
  }
}

export const forms = {
  namespaced: true,
  state,
  actions,
  getters,
  mutations
}
