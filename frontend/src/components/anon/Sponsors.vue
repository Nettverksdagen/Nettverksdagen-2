<template>
    <div class="sponsors mt-5">
      <Content>
      <!--
        <div class="sponsor-banner poption-banner">
          <a href="https://www.poption.com/speedintervju/nettverksdagene-2021" target="_blank" rel="noopener noreferrer">
            <b-row>
              <b-col cols="12" class="sponsor-banner-text align-middle">
                <h3 class="font-weight-bold">Nettverksdagene 2021 ble arrangert i samarbeid med Poption!</h3>
              </b-col>
              <b-col cols="12" lg="6" class="sponsor-banner-text align-middle no-padding-top">
                <span>Poption setter deg i kontakt med de mest interessante bedriftene &mdash; fra startups til veletablerte selskaper. Trykk på banneret for å se årets speedintervjuer i samarbeid med Poption!</span>
              </b-col>
              <b-col cols="12" lg="6" class="text-center no-padding-top">
                <img class="logo-poption float-lg-right" src="@/assets/poption.png">
              </b-col>
            </b-row>
          </a>
        </div>
        -->
        <!--<div class="sponsor-banner bunnpris-banner">
            <a href="https://bunnpris.no/" target="_blank" rel="noopener noreferrer">
                <b-row>
                    <b-col cols="12" md="6" class="sponsor-banner-text align-middle">
                        <h3 class="font-weight-bold">{{$t('thanksbunn')}}</h3>
                        <span>{{$t('thanksbunntext')}}</span>
                    </b-col>
                    <b-col cols="12" md="6" class="text-center">
                        <img class="logo-bunnpris float-md-right" src="@/assets/bunnpris.png">
                    </b-col>
                </b-row>
            </a>
        </div> -->
        <h2 class="text-center font-weight-bold">Hovedsponsor</h2>
        <div class="sponsor col-5">
          <a href="https://nfea.no/" target="_blank" rel="noopener noreferrer">
            <b-img fluid src="@/assets/nfea.png"></b-img>
          </a>
        </div>
        <h2 class="text-center font-weight-bold">{{ $t('coffeesponsor') }}</h2>
        <div class="sponsor col-5">
            <a href="https://teogkaffehuset.no/" target="_blank" rel="noopener noreferrer">
                <b-img fluid src="@/assets/teogkaffehuset.png"></b-img>
            </a>
        </div>
        <h2 class="text-center font-weight-bold" style="margin-top: 4rem;">Øvrige sponsorer</h2>
        <b-row>
          <Sponsor  v-for="(sponsor, index) in sponsors"
          :key="index"
          :logo_src="sponsor.logo_uri"
          :href="sponsor.website_url">
          </Sponsor>
        </b-row>
      </Content>
    </div>
</template>

<script>
import Content from '@/components/common/Content.vue'
import Sponsor from '@/components/anon/Sponsor.vue'
export default {
  name: 'Sponsors',
  components: { Content, Sponsor },
  computed: {
    sponsors: function () {
      return this.$store.state.sponsors.all
    }
  }
}
</script>

<style lang="scss" scoped>
  h2 {
    font-size: 1.5rem;
    font-weight: 700;
    text-align: center;
    color: var(--primary-color);
    margin-bottom: 30px;
    @media(min-width: 1200px) {
      margin-bottom: 50px;
    }
    @media(min-width: 576px) {
      font-size: 2.0rem;
    }
    @media(min-width: 768px) {
      font-size: 2.5rem;
    }
  }
  .sponsor {
    position: relative;
    margin: auto;
    transition: transform 300ms, filter 500ms;
    padding: 1rem 1rem;
      @media(min-width: 576px) {
        padding: 0rem 3rem;
      }
      @media(min-width: 1200px) {
        padding: 0.5rem 5.25rem;
      }
  }
  .sponsor:hover {
    transition: filter 0.5s, transform 0.3s;
    @media(min-width: 1200px) {
      filter: none;
    }
  }
  .sponsor-banner {
    margin: 2rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.16), 0 2px 5px rgba(0,0,0,0.15);
    transition: 0.2s;
    &:hover {
      box-shadow: 0 5px 10px rgba(0,0,0,0.20), 0 5px 10px rgba(0,0,0,0.18);
    }
    a {
      text-decoration:none;
      color: inherit;
    }
    @media(max-width: 576px) {
      margin: 1rem;
    }
  }
  .sponsor-banner-text {
    padding: 3rem 4rem;
    h3 {
      color: #221e1f;
      margin-bottom: 0.5rem;
      font-size: 1.9rem;
    }
    span {
      font-size: 1.2rem;
    }
    @media(max-width: 576px) {
      padding: 1.5rem 2.5rem;
      span {
        font-size: 0.9rem;
      }
      h3 {
        font-size: 1.5rem;
      }
    }
    @media(max-width: 768px) {
      padding-bottom: 0;
    }
  }
  .no-padding-top {
    padding-top:0;
  }

</style>
