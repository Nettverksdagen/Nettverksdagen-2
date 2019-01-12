<template>
    <div class="sponsors mt-5">
      <Content>
        <h2 class="text-center font-weight-bold">Våre sponsorer</h2>
        <div class="sponsor-banner">
          <a href="http://kjeldsbergkaffe.no/" target="_blank" rel="noopener noreferrer">
            <b-row>
              <b-col cols="12" md="6" class="sponsor-banner-text align-middle">
                <h3 class="font-weight-bold">Takk til Kjeldsberg Kaffe!</h3>
                <span>Vi takker Kjeldsberg Kaffe for årets forsyning av kaffe under hele Nettverksdagen 2019!</span>
              </b-col>
              <b-col cols="12" md="6" class="text-center">
                <img class="logo-kjeldsberg float-md-right" src="@/assets/kjeldsberg.png">
              </b-col>
            </b-row>
          </a>
        </div>
        <b-row>
          <Sponsor v-for="(sponsor, index) in sponsors"
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
  data: function () {
    return {
      sponsors: []
    }
  },
  mounted: function () {
    this.$data.sponsors = this.$store.state.sponsors.all
  }
}
</script>

<style lang="scss" scoped>
  .sponsor-banner {
    background-color: #ffd600;
    margin: 2rem 2rem 0 2rem;
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
  }
  .sponsor-banner-text {
    padding: 3rem 4rem;

    @media(max-width: 768px) {
      padding-bottom: 0;
    }

    h3 {
      color: #221e1f;
      margin-bottom: 0.5rem;
    }
  }
  .logo-kjeldsberg {
    height: 11rem;
    padding: 0.5rem 3rem 1rem 3rem;

    @media(max-width: 576px) {
      height: 7.5rem;
      padding: 1rem;
    }
  }
</style>
