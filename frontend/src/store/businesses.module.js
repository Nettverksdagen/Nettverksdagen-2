const defaultState = {
  all: []
}

const state = {...defaultState}

const actions = {
  async fetchBusinesses ({commit}) {
    commit('fetchRequest')

    try {
      const response = await fetch(process.env.VUE_APP_API_HOST + '/api/business/')
      const all = await response.json()
      commit('fetchSuccessful', all)
    } catch (e) {
      commit('fetchFailure', e)
    }
  }
}

const getters = {
  levels: state => {
    let levels = {}
    for (let i = 0; i < state.all.length; i++) {
      if (!(state.all[i].level in levels)) {
        levels[state.all[i].level] = {
          level: state.all[i].level,
          businesses: [state.all[i]]
        }
      } else {
        levels[state.all[i].level]['businesses'].push(state.all[i])
      }
    }
    return levels
  }
}

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
