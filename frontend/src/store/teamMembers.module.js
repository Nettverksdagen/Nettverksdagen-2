const defaultState = {
  all: []
}

const state = {...defaultState}

const actions = {
  async fetchTeamMembers ({commit}) {
    commit('fetchRequest')

    try {
      const response = await fetch(process.env.VUE_APP_API_HOST + '/api/teammember/')
      const all = await response.json()
      commit('fetchSuccessful', all)
    } catch (e) {
      commit('fetchFailure', e)
    }
  }
}

const getters = {
  teams: state => {
    let teams = {}
    for (let i = 0; i < state.all.length; i++) {
      if (!(state.all[i].team in teams)) {
        teams[state.all[i].team] = {
          name: state.all[i].team,
          members: [state.all[i]]
        }
      } else {
        teams[state.all[i].team]['members'].push(state.all[i])
      }
    }

    Object.keys(teams).forEach(teamKey => {
      teams[teamKey].members.sort((a, b) => a.id - b.id)
    })
    return teams
  }
}

const mutations = {
  fetchRequest (state) {
    state.loaded = false
    state.loading = true
  },
  fetchSuccessful (state, teamMembers) {
    state.all = teamMembers
    state.loading = false
    state.loaded = true
  },
  fetchFailure () {
    console.log('Failed to fetch team members')
  },
  addTeamMember (state, teamMember) {
    state.all.push(teamMember)
  },
  deleteTeamMember (state, teamMember) {
    state.all = state.all.filter(tm => tm.id !== teamMember.id)
  },
  updateTeamMember (state, teamMember) {
    const modify = state.all.findIndex(tm => tm.id === teamMember.id)
    state.all[modify] = teamMember
  }
}

export const teamMembers = {
  namespaced: true,
  state,
  actions,
  getters,
  mutations
}
