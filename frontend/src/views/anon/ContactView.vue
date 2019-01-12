<template>
  <div class="contact-view">
    <Content>
      <h1>Kontakt oss</h1>

      <hr>

      <b-row>
        <b-col cols="12" md="5">
          <h2>Våre viktigste kanaler</h2>
          <p class="description">
            Bruk disse kanalene hvis du ikke vet hvem du skal kontakte i Nettverksdagen.
            Lenger ned på siden finnes det en oversikt over kontaktpersoner og deres stillinger hvis du heller vil
            kontakte noen direkte.
          </p>
        </b-col>
        <b-col cols="12" md="7">
          <b-card>
          <table class="main-contact">
            <tr>
              <td class="align-top">
                <h3>Styret</h3>
                <b-link href="mailto:styret@nvdagen.no">styret@nvdagen.no</b-link>
              </td>
              <td>
                <p>
                  Har du generelle henvendelser, eller er usikker på hvem du skal kontakte, kan du kontakte styret direkte.
                </p>
              </td>
            </tr>

            <tr>
              <td class="align-top">
                <h3>Bedrift</h3>
                <b-link href="mailto:bedrift@nvdagen.no">bedrift@nvdagen.no</b-link>
              </td>
              <td>
                <p>
                  Ønsker din bedrift å vise seg fram på Nettverksdagen,
                  har dere allerede en avtale med oss,
                  eller har dere andre henvendelser angående bedriftspotlight, bedriftpresentasjon, stand osv,
                  ta kontakt med bedriftgruppa.
                </p>
              </td>
            </tr>

            <tr>
              <td class="align-top">
                <h3>Sponsor</h3>
                <b-link href="mailto:sponsor@nvdagen.no">sponsor@nvdagen.no</b-link>
              </td>
              <td>
                <p>
                  For henvendelser angående sponsorsamarbeid, kontakt sponsorgruppa.
                </p>
              </td>
            </tr>
          </table>
          </b-card>
        </b-col>
      </b-row>

      <Spacer/>

      <b-row class="mt-5">
        <b-col cols="12">
          <h2>Kontaktpersoner</h2>
        </b-col>
      </b-row>
        <hr>
        <b-row v-bind:key="team.key" v-for="team in teams">
          <b-col cols="12">
            <h3 class="font-weight-bold">{{ team.name }}</h3>
          </b-col>
          <b-col class="my-md-3 my-1" cols="12" md="6" xl="4" v-bind:key="member.id" v-for="member in team.members">
            <b-card no-body>
              <b-card-body class="d-flex">
                <div>
                  <b-img rounded="circle" class="img-circle" :src="$options.fileServerHost + '/thumb/512/' + member.photo_uri"></b-img>
                </div>
                <div class="ml-3 d-flex justify-content-center flex-column">
                  <h4 class="member-name m-0">{{ member.name }}</h4>
                  <b-link :href="'mailto:' + member.email">{{ member.email }}</b-link>
                  <span class="font-weight-bold text-black-50">{{ member.position }}</span>
                </div>
              </b-card-body>
            </b-card>
          </b-col>
          <b-col cols="12">
            <hr>
          </b-col>
        </b-row>
    </Content>
  </div>
</template>

<script>
import Content from '@/components/common/Content.vue'
import Spacer from '@/components/common/Spacer.vue'
export default {
  name: 'ContactView',
  components: {
    Content,
    Spacer
  },
  computed: {
    teams: function () {
      return this.$store.getters['teamMembers/teams']
    }
  },
  fileServerHost: process.env.VUE_APP_FILESERVER_HOST
}
</script>

<style lang="scss" scoped>
  .description {
    font-size: 18px;
  }
  .main-contact {
    border-spacing: 5em 1em;
    td {
      @media (max-width: 575px) {
        display: table-row;
      }
    }
    h3 {
      @media (max-width: 575px) {
        font-size:1.5em;
      }
    }
    p {
      @media (min-width:768px) {
        font-size:18px;
        margin-left:1em;
      }
    }
  }
  .member-name {
    font-weight:bold;
    word-break:break-word;
  }
  .img-circle {
    height: 6rem;
  }
</style>
