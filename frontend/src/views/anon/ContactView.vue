<template>
  <div class="contact-view">
    <Content>
    <!-- <h1>{{$t('kontakt')}}</h1> -->
    <h1 class="page-header">{{$t('kontakt') + ' for ' + $t('nettverksdagene')  + ' 2025'}}</h1>
    <b-row class="firstrow">
       <!-- <b-col cols="12" md="5">
          <p class="description">
            {{$t('contactinfo')}}
          </p>
        </b-col>-->
        <b-col cols="12" md="7">
          <b-card class="overview">
          <table class="main-contact">
            <tr>
              <td class="align-top">
                <h3>{{$t('bedrift')}}</h3>
                <b-link href="mailto:bedrift@nettverksdagene.no">bedrift@nettverksdagene.no</b-link>
              </td>
              <td>
                <p class="info">
                  {{$t('doyourshow')}}
                </p>
              </td>
            </tr>

            <tr>
              <td class="align-top">
                <h3>{{$t('Styret')}}</h3>
                <b-link href="mailto:leder@nettverksdagene.no">leder@nettverksdagene.no</b-link>
              </td>
              <td>
                <p class="info">
                  {{$t('genquest')}}
                </p>
              </td>
            </tr>
            <tr>
              <td class="align-top">
                <h3>Sponsor</h3>
                <b-link href="mailto:spons@nettverksdagene.no">spons@nettverksdagene.no</b-link>
              </td>
              <td>
                <p class="info">
                  {{$t('sponsquest')}}
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
          <h1 class="page-header">{{$t('Kontaktpersoner') + ' for ' + $t('nettverksdagene')  + ' 2025'}}</h1>
        </b-col>
      </b-row>
        <b-row v-bind:key="team.key" v-for="team in teams">
            <b-col cols="12">
            <h3 class="font-weight-bold">{{ team.name }}</h3>
          </b-col>
          <b-col class="my-md-3 my-2" cols="12" md="6" xl="4" v-bind:key="member.id" v-for="member in team.members">
            <b-card no-body class="overflow-hidden columns">
              <b-card-body class="d-flex">
                <div>
                  <div v-if="member.photo_uri">
                    <b-img  rounded="circle" class="img-profile" :src="$options.fileServerHost + '/thumb/512/' + member.photo_uri"></b-img>
                  </div>
                  <div v-else>
                    <b-img  rounded="circle" class="img-profile-empty" :src="'https://d2ojdbp0769afo.cloudfront.net/fnd/v4/static/images/BlankProfile.png'"></b-img>
                  </div>
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
  .contact-view {
    flex: 1;
  }
  .firstrow {
    margin-bottom: -40px;
  }
  .description {
    font-size: 18px;
    text-align: center;
    @media(min-width: 768px) {
      text-align: left;
    }
  }
  .info {
    margin-left: 0px;
    @media(min-width: 768px) {
      margin-left: 10px;
    }
  }
  h2 {
    text-align: center;
    @media(min-width: 768px) {
      text-align: left;
    }
  }
  .overview {
    border-radius: 20px;
    border-width: 2px;
    border-color: var(--line-border-color);
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
        // margin-left:1em;
      }
    }
  }
  .columns {
    color: var(--primary-color);
    border-radius: 20px;
    background-color: white;
    border-width: 2px;
    border-color: var(--line-border-color);
    text-align: left;
    margin-bottom: -10px;
  }
  .member-name {
    font-weight: bold;
    word-break: break-word;
  }
  .member-email {
    word-break: break-word;
    font-size: 14px;
    @media (min-width: 992px) {
      font-size: 16px;
    }
  }
  .img-profile-empty {
    align-self: center;
    height: 50px;
    width: 50px;
    //box-shadow: 0 1px 2px rgba(0,0,0,0.3);
  }
  .img-profile{
    align-self: center;
    height: 6rem;
    width: 6rem;
    //box-shadow: 0 1px 2px rgba(0,0,0,0.3);
  }
</style>
