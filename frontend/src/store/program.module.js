const defaultState = {
    all: []
  }
  
  const state = {...defaultState}
  
  const actions = {
    async fetchProgram ({commit}) {
      commit('fetchRequest')
      try {
        const response = await fetch(process.env.VUE_APP_API_HOST + '/api/program/')
        const all = await response.json()
        commit('fetchSuccessful', all)
      } catch (e) {
        commit('fetchFailure', e)
      }
    }
  }
  
  const getters = {
    // formatting program as needed
    anonProgram: state =>  {
        let programItems = [];
        state.all.forEach((item) => {
          let newItem = {};
            Object.keys(item).forEach((key) => {
              newItem[key] = item[key]
            })
           
            newItem.timeStart = new Date(item.timeStart*1000)
            if (item.timeEnd) {
                newItem.timeEnd = new Date(item.timeEnd*1000)
            }
            newItem.paragraph=String(item.paragraph).split('\n');
            
            if (item.registration) {
                newItem.registrationStart = new Date(item.registrationStart*1000)
                if (item.registrationEnd) {
                    newItem.registrationEnd = new Date(item.registrationEnd*1000)
                }
            }
            programItems.push(newItem)
        })
        return programItems
        // Return the program formated as ProgramView needs it
    },
    adminProgram: state =>  {
        let programItems = [];
        state.all.forEach((item) => {
            let newItem = item;
            newItem.paragraph = String(item.paragraph).split('\n');
            newItem.timeStart = new Date(item.timeStart*1000)
            let month = String(newItem.timeStart.getMonth() + 1);
            month = (month.length < 2) ? "0" + month : month;
            let day = String(newItem.timeStart.getDay());
            day = (day.length < 2) ? "0" + day : day;
            newItem.date = String(newItem.timeStart.getFullYear()) + "-" + month + "-" + day;
            let hour = String(newItem.timeStart.getHours())
            hour = (hour.length < 2) ? "0" + hour : hour
            let min = String(newItem.timeStart.getMinutes())
            min = (min.length < 2) ? "0" + min : min
            newItem.timeStart = hour + ":" + min
            if (item.timeEnd) {
                newItem.timeEnd = new Date(item.timeEnd*1000);
                let hour = String(newItem.timeEnd.getHours())
                hour = (hour.length < 2) ? "0" + hour : hour
                let min = String(newItem.timeEnd.getMinutes())
                min = (min.length < 2) ? "0" + min : min
                newItem.timeEnd = hour + ":" + min
            }

            if (item.registration) {
                newItem.registrationStart = new Date(item.registrationStart*1000)                
                let month = String(newItem.registrationStart.getMonth() + 1);
                month = (month.length < 2) ? "0" + month : month;
                let day = String(newItem.registrationStart.getDay());
                day = (day.length < 2) ? "0" + day : day;
                newItem.registrationStartDate = String(newItem.registrationStart.getFullYear()) + "-" + month + "-" + day

                let hour = String(newItem.registrationStart.getHours())
                hour = (hour.length < 2) ? "0" + hour : hour
                let min = String(newItem.registrationStart.getMinutes())
                min = (min.length < 2) ? "0" + min : min
                newItem.registrationStartTime = hour + ":" + min


                if (item.registrationEnd) {
                    newItem.registrationEnd = new Date(item.registrationEnd*1000);
                    
                    let month = String(newItem.registrationEnd.getMonth() + 1);
                    month = (month.length < 2) ? "0" + month : month;
                    let day = String(newItem.registrationEnd.getDay());
                    day = (day.length < 2) ? "0" + day : day;
                    newItem.registrationEndDate = String(newItem.registrationEnd.getFullYear()) + "-" + month + "-" + day

                    let hour = String(newItem.registrationEnd.getHours())
                    hour = (hour.length < 2) ? "0" + hour : hour
                    let min = String(newItem.registrationEnd.getMinutes())
                    min = (min.length < 2) ? "0" + min : min
                    newItem.registrationEndTime = hour + ":" + min
                }
            }
            programItems.push(newItem)
        })
        return programItems
        // Return the program formated as ProgramAdminView needs it
    }
  }
  
  const mutations = {
    fetchRequest (state) {
      state.loaded = false
      state.loading = true
    },
    fetchSuccessful (state, program) {
      state.all = program
      state.loading = false
      state.loaded = true
    },
    fetchFailure () {
      console.log('Failed to fetch program')
    },
    addProgramItem (state, programItem) {
      state.all.push(programItem)
    },
    deleteProgramItem  (state, programItem) {
      state.all = state.all.filter(pi => pi.id !== programItem.id)
    },
    updateProgramItem  (state, programItem) {
      const modify = state.all.findIndex(pi => pi.id === programItem.id)
      state.all[modify] = programItem
    }
  }
  
  export const program = {
    namespaced: true,
    state,
    actions,
    getters,
    mutations
  }