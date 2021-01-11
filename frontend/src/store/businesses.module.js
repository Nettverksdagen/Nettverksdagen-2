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
    let levels = [
      {level: 'Hovedsamarbeidspartner', levelHeader: 'Hoved&shy;samarbeids&shy;partner', businesses: []},
      {level: 'Samarbeidspartner', levelHeader: 'Samarbeids&shy;partnere', businesses: []},
      {level: 'Gull', levelHeader: 'Bedrifter du kan møte på stand', businesses: []},
      {level: 'Sølv', levelHeader: '', businesses: []},
      {level: 'Bronse', levelHeader: '', businesses: []}
    ]
    for (let i = 0; i < state.all.length; i++) {
      for (let j = 0; j < levels.length; j++) {
        if (state.all[i].level === levels[j].level) {
          levels[j].businesses.push(state.all[i])
          break
        }
      }
    }
    return levels
  },
  days: state => {
    let days = [
      {day: 'Dag 1', dayHeader: 'Bedrifter du kan møte på digital stand 27. januar'}
      // {day: 'Dag 2', dayHeader: 'Bedrifter du kan møte på stand 28. januar'}
    ]
    for (let i = 0; i < days.length; i++) {
      days[i]['levels'] = [
        {level: 'Hovedsamarbeidspartner', businesses: []},
        {level: 'Samarbeidspartner', businesses: []},
        {level: 'Gull', businesses: []},
        {level: 'Sølv', businesses: []},
        {level: 'Bronse', businesses: []}
      ]
    }
    for (let i = 0; i < state.all.length; i++) {
      for (let j = 0; j < days.length; j++) {
        for (let k = 0; k < days[j].levels.length; k++) {
          if (state.all[i].level === days[j].levels[k].level && (state.all[i].days === days[j].day || state.all[i].days === 'Begge dager')) {
            days[j].levels[k].businesses.push(state.all[i])
          }
        }
      }
    }
    return days
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
  },
  deleteBusiness (state, business) {
    state.all = state.all.filter(bus => bus.id !== business.id)
  },
  updateBusiness (state, business) {
    const modify = state.all.findIndex(bus => bus.id === business.id)
    state.all[modify] = business
  }
}

export const businesses = {
  namespaced: true,
  state,
  actions,
  getters,
  mutations
}
