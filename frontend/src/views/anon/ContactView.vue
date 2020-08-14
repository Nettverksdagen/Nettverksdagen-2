<template>
  <div class="contact-view">
    <Content>
      <h1>Kontakt oss</h1>

      <hr>

      <b-row>
        <b-col cols="12" md="5">
          <h2>Våre viktigste kanaler</h2>
          <p class="description">
            Bruk disse kanalene til å kontakte oss i Nettverksdagene. Under finner du en oversikt over kontaktpersoner og deres stillinger.
          </p>
        </b-col>
        <b-col cols="12" md="7">
          <b-card>
          <table class="main-contact">
            <tr>
              <td class="align-top">
                <h3>Styret</h3>
                <b-link href="mailto:leder@nettverksdagene.no">leder@nettverksdagene.no</b-link>
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
                <b-link href="mailto:bedrift@nettverksdagene.no">bedrift@nettverksdagene.no</b-link>
              </td>
              <td>
                <p>
                  Ønsker din bedrift å vise seg fram på Nettverksdagene,
                  har dere allerede en avtale med oss,
                  eller har dere andre henvendelser angående bedriftspotlight, bedriftpresentasjon, stand osv,
                  ta kontakt med bedriftgruppa.
                </p>
              </td>
            </tr>

            <tr>
              <td class="align-top">
                <h3>Sponsor</h3>
                <b-link href="mailto:spons@nettverksdagene.no">spons@nettverksdagene.no</b-link>
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
          <h2>Kontaktpersoner for Nettverksdagene 2021</h2>
        </b-col>
      </b-row>
        <hr>
        <b-row v-bind:key="team.key" v-for="team in teams">
          <b-col cols="12">
            <h3 class="font-weight-bold">{{ team.name }}</h3>
          </b-col>
          <b-col class="my-md-3 my-1" cols="12" md="6" xl="4" v-bind:key="member.id" v-for="member in team.members">
            <b-card no-body class="overflow-hidden">
              <b-card-body class="d-flex">
                <div>
                  <b-img  rounded="circle" class="img-profile" :src="memberPhoto(member)"></b-img>
                </div>
                <div class="ml-3 d-flex justify-content-center flex-column">
                  <h4 class="member-name m-0">{{ member.name }}</h4>
                  <b-link class="member-email" :href="'mailto:' + member.email">{{ member.email }}</b-link>
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
  methods: {
    memberPhoto (member) {
      if (member.photo_uri) {
        return process.env.VUE_APP_FILESERVER_HOST + '/thumb/512/' + member.photo_uri
      } else {
        return 'https://d2ojdbp0769afo.cloudfront.net/fnd/v4/static/images/BlankProfile.png'
      }
    }
  },
  computed: {
    teams: function () {
      // use this line to get teams from database:
      // return this.$store.getters['teamMembers/teams']
      let hardCodedTeams = [
        {
          key: 'styret',
          name: 'Styret',
          members: [{id: 'styret1', name: 'Marie Øverby', email: 'leder@nettverksdagene.no', position: 'Leder'},
            {id: 'styret2', name: 'Magne Angvik Hovdar', email: 'it@nettverksdagene.no', position: 'IT-ansvarlig'},
            {id: 'styret3', name: 'Helene Semb', email: 'spons@nettverksdagene.no', position: 'Sponsoransvarlig'},
            {id: 'styret4', name: 'Nina Nyegaarden', email: 'bedrift@nettverksdagene.no', position: 'Bedriftsansvarlig'},
            {id: 'styret5', name: 'Eskil Ould-Saada', email: 'markedsfoering@nettverksdagene.no', position: 'Markedsføringsansvarlig'},
            {id: 'styret6', name: 'Mari Linnerud', email: 'logistikk@nettverksdagene.no', position: 'Logistikkansvarlig'}]
        },
        {
          key: 'bedriftskontaker',
          name: 'Bedrift',
          members: [{id: 'bedrift1', name: 'Eivind Dogger', email: 'eivindd@nettverksdagene.no', position: 'Bedriftskontakt'},
            {id: 'bedrift2', name: 'Erling Syvervseen Lie', email: 'erlingsl@nettverksdagene.no', position: 'Bedriftskontakt'},
            {id: 'bedrift3', name: 'Fred Kwizera', email: 'fredk@nettverksdagene.no', position: 'Bedriftskontakt'},
            {id: 'bedrift4', name: 'Hanne Opseth Rygg', email: 'hanneor@nettverksdagene.no', position: 'Bedriftskontakt'},
            {id: 'bedrift5', name: 'Helene Engebakken Haugen', email: 'heleneeh@nettverksdagene.no', position: 'Bedriftskontakt'},
            {id: 'bedrift6', name: 'Henrik Larsson Hestnes', email: 'henriklh@nettverksdagene.no', position: 'Bedriftskontakt'},
            {id: 'bedrift7', name: 'Kristoffer Eikså', email: 'kristoffere@nettverksdagene.no', position: 'Bedriftskontakt'},
            {id: 'bedrift8', name: 'Lars Eik Breirem', email: 'larseb@nettverksdagene.no', position: 'Bedriftskontakt'},
            {id: 'bedrift9', name: 'Lasse Wardenær', email: 'lassetw@nettverksdagene.no', position: 'Bedriftskontakt'},
            {id: 'bedrift10', name: 'Maja Markusson', email: 'majam@nettverksdagene.no', position: 'Bedriftskontakt'},
            {id: 'bedrift11', name: 'Marie Gjerden', email: 'marieg@nettverksdagene.no', position: 'Bedriftskontakt'},
            {id: 'bedrift12', name: 'Marte Aaberge', email: 'marteka@nettverksdagene.no', position: 'Bedriftskontakt'},
            {id: 'bedrift13', name: 'Mathias Grindvik', email: 'mathiasg@nettverksdagene.no', position: 'Bedriftskontakt'},
            {id: 'bedrift14', name: 'Ole Andreas Wammer', email: 'oleaw@nettverksdagene.no', position: 'Bedriftskontakt'},
            {id: 'bedrift15', name: 'Yngve Kippersund', email: 'yngvek@nettverksdagene.no', position: 'Bedriftskontakt'}]
        }
      ]
      return hardCodedTeams
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
  .member-email {
    font-size: 13px;
  }
  .img-profile {
    align-self: center;
    height: 50px;
    width: 50px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.3);
  }
</style>
