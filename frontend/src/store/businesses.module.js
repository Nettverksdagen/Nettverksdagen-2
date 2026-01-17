import { i18n } from '../translations/translations'

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
    // map backend level values (used for matching) to translated labels/headers
    const levelMap = [
      { value: 'Hovedsamarbeidspartner', label: i18n.t('businesses.levels.main'), header: i18n.t('businesses.mainPartnerHeader'), businesses: [] },
      { value: 'Samarbeidspartner', label: i18n.t('businesses.levels.partner'), header: i18n.t('businesses.partnersHeader'), businesses: [] },
      { value: 'Gull', label: i18n.t('businesses.levels.gold'), header: i18n.t('businesses.standHeader'), businesses: [] },
      { value: 'Sølv', label: i18n.t('businesses.levels.silver'), header: '', businesses: [] },
      { value: 'Bronse', label: i18n.t('businesses.levels.bronze'), header: '', businesses: [] },
      { value: 'Startup', label: i18n.t('businesses.levels.startup'), header: '', businesses: [] }
    ]

    for (let i = 0; i < state.all.length; i++) {
      for (let j = 0; j < levelMap.length; j++) {
        if (state.all[i].level === levelMap[j].value) {
          levelMap[j].businesses.push(state.all[i])
          break
        }
      }
    }
    return levelMap
  },
  days: state => {
    // days.day is used for matching against backend values; dayLabel/dayHeader are translated for UI
    let days = [
      { day: 'Dag 1', dayLabel: i18n.t('businesses.days.day1'), dayHeader: i18n.t('businesses.days.dayHeader') },
      { day: 'Dag 2', dayLabel: i18n.t('businesses.days.day2'), dayHeader: i18n.t('businesses.days.dayHeader') }
    ]

    for (let i = 0; i < days.length; i++) {
      days[i]['levels'] = [
        {level: 'Hovedsamarbeidspartner', label: i18n.t('businesses.levels.main'), businesses: []},
        {level: 'Samarbeidspartner', label: i18n.t('businesses.levels.partner'), businesses: []},
        {level: 'Gull', label: i18n.t('businesses.levels.gold'), businesses: []},
        {level: 'Sølv', label: i18n.t('businesses.levels.silver'), businesses: []},
        {level: 'Bronse', label: i18n.t('businesses.levels.bronze'), businesses: []},
        {level: 'Startup', label: i18n.t('businesses.levels.startup'), businesses: []}
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
