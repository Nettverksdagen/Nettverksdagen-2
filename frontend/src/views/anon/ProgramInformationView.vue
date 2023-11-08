<template>
    <Content>

        <div>
            <h1 class="text-center">Title</h1>

            <div class="container">
                <div class="two-thirds">
                    <h1 class="text-center">SmallTitle</h1>
                </div>
                <div class="one-third">
                    <div class="sub-box">
                        <b-button v-if="enableRegistration && !submitted" variant='primary' @click="openDialog">{{$t('påmelding')}}</b-button>
                        <b-button v-else disabled variant="dark">{{$t('påmelding')}}</b-button>
                    </div>
                    <div class="sub-box">
                        <p>Content for the second 1/3 sub-box</p>
                    </div>
                    <div class="sub-box">
                        <p>Content for the third 1/3 sub-box</p>
                    </div>
                </div>
            </div>
        </div>
    </Content>
</template>



<script>
import ProgramItem from '@/components/anon/ProgramItem.vue'
import axios from 'axios'
// import { mapMutations } from 'vuex'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMapMarkerAlt, faClock } from '@fortawesome/free-solid-svg-icons'

library.add(faMapMarkerAlt, faClock)
export default {
    name: 'ProgramInformationView',
    components: {
        ProgramItem
    },
    data: function () {
        return {
            program: []
        }
    },
    mounted: function () {
        this.$data.program = this.$store.state.program.all
        console.log(this.$data.program)
    },
    computed: {
        registered: function () {
            return this.$store.state.participant.all.filter(par => par.event === this.$props.name).length
        },
        beforeRegistration: function () {
            let now = new Date()
            return this.$props.registrationStart.getTime() > now.getTime()
        },
        afterRegistration: function () {
            let now = new Date()
            if (this.$props.registrationEnd) {
                return this.$props.registrationEnd.getTime() < now.getTime()
            }
            return this.$props.timeStart.getTime() < now.getTime()
        },
        enableRegistration: function () {
            if (!this.$props.registration) {
                return false
            }
            if (this.beforeRegistration) {
                return false
            }
            if (this.afterRegistration) {
                return false
            }
            return true
        }
    },
    methods: {
        formatTime(dateObj) {
            let hours = dateObj.getHours()
            let minutes = dateObj.getMinutes()
            hours = (hours > 9) ? String(hours) : ('0' + String(hours))
            minutes = (minutes > 9) ? String(minutes) : ('0' + String(minutes))
            return hours + ':' + minutes
        },
        formatDate(dateObj) {
            let day = dateObj.getDate()
            let month = dateObj.getMonth() + 1
            let year = dateObj.getFullYear()
            day = (day > 9) ? String(day) : ('0' + String(day))
            month = (month > 9) ? String(month) : ('0' + String(month))
            return this.formatTime(dateObj) + ' ' + day + '.' + month + '.' + year
        },
        openDialog() {
            this.$data.form = { email: '', name: '', study: '', year: '' }
            this.$data.show = true
        },
        onSubmit(e) {
            e.preventDefault()
            let data = this.$data.form
            // Generate and include 6-character random deregistering code
            data.code = Array(6).fill(0).map(x => Math.random().toString(36).charAt(2)).join('').toUpperCase()
            if (this.checkValidForm(data)) {
                this.submitForm()
                // Clear data
                this.$data.show = false
                this.$data.form = { email: '', name: '', study: '', year: '' }
                this.$data.submitted = true
            }
        },
        submitForm() {
            console.log({ event: this.$props.name, ...this.$data.form })
            axios.post(process.env.VUE_APP_API_HOST +
                '/api/participant/', { event: this.$props.name, ...this.$data.form })
                .then((response) => console.log(response))
                .catch((e) => {
                    console.log('Error in submitForm')
                    console.log(e)
                })
        },
        onCancel(e) {
            e.preventDefault()
            this.$data.form = { email: '', name: '', study: '', year: '' }
            this.$data.show = false
        },
        checkValidForm(check) {
            for (let key in check) {
                if (check[key] === '') {
                    return false
                } else if (key === 'email') {
                    let at = check[key].split('@')
                    let dot = at[at.length - 1].split('.')
                    if (at.length < 2 || dot.length < 2 || dot[dot.length - 1].length === 0) {
                        return false
                    }
                }
            }
            return true
        },
        destroy_participant: function (event) {
            let email = prompt('Vennligst skriv inn emailen din:')
            let participants = this.$store.state.participant.all
            let participant = participants.filter(par => par.email === email && par.event === event)[0]

            if (participant !== undefined) {
                // Send deregistering code
                let code = participant.code
                axios.get(process.env.VUE_APP_API_HOST + '/api/participant/' +
                    participant.id + '/').then(_ => {
                        // Prompt user for code, and delete participant if input matches
                        let retry = true
                        while (retry) {
                            let inputedCode = prompt('Vennligst skriv inn koden som ble sendt til ' + participant.email + '. Hvis du ikke mottar mailen, vennligst kontakt IT-gruppen på it@nettverksdagene.no.')
                            if (inputedCode === code) {
                                if (confirm('Er du sikker på at du vil melde av ' + participant.name + '?')) {
                                    axios.delete(process.env.VUE_APP_API_HOST + '/api/participant/' +
                                        participant.id + '/').then(_ => {
                                            alert(participant.name + ' er nå avmeldt.')
                                        }).catch(_ => {
                                            alert('Det oppsto en feil under avmeldingen. Vennligst kontakt IT-gruppen på it@nettverksdagene.no.')
                                        })
                                }
                                break
                            } else {
                                retry = confirm('Feil kode. Vil du prøve igjen?')
                            }
                        }
                    }).catch(_ => {
                        alert('Det oppsto en feil under sendingen av avmeldingskoden. Vennligst kontakt IT-gruppen på it@nettverksdagene.no.')
                    })
            } else if (email !== null) {
                alert('Fant ingen deltakere med denne epost-adressen på dette arrangementet.')
            }
        }
    },
}
</script>



<style scoped lang="scss">
.container {
    display: flex;
    width: 100%;
}

.card {
    position: relative;
    border-radius: 20px;
    border-width: 2px;
    border-color: var(--line-border-color);
    background-color: white;
}

.two-thirds {
    flex: 2;
    background-color: white;
    padding: 10px;
    /* Reduce padding for better space management */
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 20px;
}

.one-third {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: white;
    padding: 10px;
    /* Reduce padding for better space management */
    overflow-y: auto;
    /* Enable vertical scrolling if content exceeds box height */
    max-height: 100%;
    /* Set a maximum height for the box */
}

.sub-box {
    flex: 1;
    background-color: white;
    border: 1px solid rgba(0, 0, 0, 0.1);
    padding: 10px;
    /* Reduce padding for better space management */
    margin-bottom: 10px;
    overflow-y: auto;
    /* Enable vertical scrolling if content exceeds box height */
    border-radius: 20px;
}
</style>
