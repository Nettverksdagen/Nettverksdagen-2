<template>
  <div class="anon-footer">
    <Content class="text-md-left text-center">
      <b-row>
        <b-col cols="12" sm="12" md="6" lg="6" class="mb-sm-0 mb-3">
          <div class="d-md-flex">
            <div>
              <img class="img-logo mb-md-0 mb-3" src="@/assets/nettverksdagenesvg.svg"/>
            </div>
            <div>
              <h5>{{$t('nettverksdagene')}}</h5>
              <p class="text-subtle mr-3">{{$t('hensikt')}}</p>
            </div>
          </div>
        </b-col>

        <b-col cols="12" sm="12" md="3" lg="3" class="mb-sm-0 mb-3">
          <h5>{{$t('kontakt')}}</h5>
          <ul class="list-unstyled">
            <li><span class="font-weight-bold">{{$t('Styret')}}:</span> <a class="green-link" href="mailto:leder@nettverksdagene.no">leder@nettverksdagene.no</a></li>
            <li><span class="font-weight-bold">{{$t('Bedrift')}}:</span> <a class="green-link" href="mailto:bedrift@nettverksdagene.no">bedrift@nettverksdagene.no</a></li>
            <li><span class="font-weight-bold">Sponsor:</span> <a class="green-link" href="mailto:spons@nettverksdagene.no">spons@nettverksdagene.no</a></li>
          </ul>
        </b-col>

        <b-col cols="12" sm="12" md="3" lg="3" class="text-md-right">
          <h5>{{$t('folgos')}}</h5>
          <ul class="list-inline social-icons">
            <li class="list-inline-item facebook">
              <a href="https://www.facebook.com/nvdagene/" target="_blank">
                <font-awesome-icon :icon="{ prefix: 'fab', iconName: 'facebook' }" size="lg"/>
              </a>
            </li>
            <li class="list-inline-item linkedin">
              <a href="https://www.linkedin.com/company/nettverksdagen-ntnu" target="_blank">
                <font-awesome-icon :icon="{ prefix: 'fab', iconName: 'linkedin' }" size="lg"/>
              </a>
            </li>
            <li class="list-inline-item instagram">
              <a href="https://www.instagram.com/nettverksdagene_ntnu/" target="_blank">
                <font-awesome-icon :icon="{ prefix: 'fab', iconName: 'instagram' }" size="lg"/>
              </a>
            </li>
          </ul>
        </b-col>
      </b-row>
    </Content>
  </div>
</template>

<script>
import Content from '@/components/common/Content.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faFacebook, faLinkedin, faInstagram } from '@fortawesome/free-brands-svg-icons'
library.add(faFacebook, faLinkedin, faInstagram)
export default {
  name: 'AnonFooter',
  components: {
    Content
  }
}
</script>

<style scoped lang="scss">
  .anon-footer {
    width: 100%;
    margin-top: 30px;
    padding-bottom: 40px;
    @media(min-width: 1200px) {
      margin-top: 60px;
    }
    position: relative;
    background: var(--background-primary-color);
    color: var(--primary-color);
    text-align: center;
    .green-link {
      color: #388f89;
    }
    .text-subtle {
      color: var(--primary-color);
      font-weight:400;
    }
    .social-icons {
      font-size:25px;
      a {
        color: var(--primary-color);
      }
    }
  }
  h5 {
    font-weight: 600;
  }
  .img-logo{
    height: 4em;
    padding-right: 1em;
  }
  .list-inline {
    height: 20px;
  }
  .facebook {
    &:hover {
      filter: brightness(0) invert(36%) sepia(9%) saturate(3542%) hue-rotate(182deg) brightness(104%) contrast(87%);;
    }
  }
  .linkedin {
    &:hover {
      filter: brightness(0) invert(33%) sepia(95%) saturate(783%) hue-rotate(166deg) brightness(93%) contrast(108%);
    }
  }
  .instagram {
    &:hover {
      filter: brightness(0) invert(41%) sepia(82%) saturate(5689%) hue-rotate(315deg) brightness(89%) contrast(94%);
    }
  }
</style>
