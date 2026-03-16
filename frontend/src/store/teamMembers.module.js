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
  // Get an object of teams with their members, with leaders first
  teams: state => {
    let teams = {}
    for (let i = 0; i < state.all.length; i++) {
      const member = state.all[i]

      if (!(member.team in teams)) {
        teams[member.team] = {
          name: member.team,
          members: [member]
        }
      } else {
        if (member.position === 'Leder') {
          teams[member.team]['members'].unshift(member)
        } else {
          teams[member.team]['members'].push(member)
        }
      }
    }
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
