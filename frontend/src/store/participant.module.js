const defaultState = {
  all: []
}

const state = {...defaultState}

const actions = {
  async fetchParticipant ({commit}) {
    commit('fetchRequest')
    try { 
      //This must be changed to only fetch number of participants, requires changes other places first
      const response = await fetch(process.env.VUE_APP_API_HOST + '/api/participant/')
      console.log(response)
      const all = await response.json()
      console.log(all)
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
  fetchSuccessful (state, participants) {
    state.all = participants
    state.loading = false
    state.loaded = true
  },
  fetchFailure () {
    console.log('Failed to fetch participants')
  },
  addParticipant (state, participant) {
    state.all.push(participant)
  },
  deleteParticipant  (state, participant) {
    state.all = state.all.filter(pi => pi.id !== participant.id)
  },
  updateParticipant  (state, participant) {
    const modify = state.all.findIndex(pi => pi.id === participant.id)
    state.all[modify] = participant
  }
}

export const participant = {
  namespaced: true,
  state,
  actions,
  getters,
  mutations
}
