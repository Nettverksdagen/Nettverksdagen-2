<template>
  <div class="businesses mt-5">
    <Content>
      <!-- <div v-for="(level, index) in levels.slice(0,2)" :key="index" class="samarbeidspartnere">
        <h2 class="text-center font-weight-bold" v-html="levels[index].levelHeader"></h2>
        <b-row class="justify-content-center">
          <Business v-for="(business, index) in level.businesses"
                    :key="index"
                    :logo_src="business.logo_uri"
                    :href="business.website_url"
                    :text="business.text"
                    :id="business.id"
                    :name="business.name"
                    :colSize="$options.sizesLevels[business.level]">
          </Business>
        </b-row>
        <hr>
      </div> -->
      <h2 class="text-center font-weight-bold">Bedrifter du kan møte på stand</h2>
      <div v-for="(day, dindex) in days" :key="'day' + dindex">
        <b-row class="justify-content-center">
          <template v-for="(level, lindex) in days[dindex].levels">
            <Business v-for="business in days[dindex].levels[lindex].businesses"
                      :key="business.id"
                      :logo_src="business.logo_uri"
                      :href="business.website_url"
                      :text="business.text"
                      :id="business.id"
                      :name="business.name"
                      :colSize="$options.sizesDays[business.level]">
            </Business>
          </template>
        </b-row>
      </div>
      <hr>
    </Content>
    <router-view />
  </div>
</template>

<script>
import Content from '@/components/common/Content.vue'
import Business from '@/components/anon/Business.vue'
export default {
  name: 'Businesses',
  components: { Content, Business },
  data: function () {
    return {
      businesses: []
    }
  },
  mounted: function () {
    this.$data.businesses = this.$store.state.businesses.all
  },
  computed: {
    levels: function () {
      return this.$store.getters['businesses/levels']
    },
    days: function () {
      return this.$store.getters['businesses/days']
    }
  },
  sizesLevels: {
    'Hovedsamarbeidspartner': 'very_big',
    'Samarbeidspartner': 'big',
    'Gull': 'big',
    'Sølv': 'medium',
    'Bronse': 'small'
  },
  sizesDays: {
    'Hovedsamarbeidspartner': 'medium',
    'Samarbeidspartner': 'medium',
    'Gull': 'medium',
    'Sølv': 'medium',
    'Bronse': 'medium'
  }
}
</script>

<style lang="scss" scoped>
  h2 {
    font-size: 1.5rem;
    overflow-wrap: break-word;
    color: var(--primary-color);
    @media(min-width: 576px) {
      font-size: 2.0rem;
    }
    @media(min-width: 768px) {
      font-size: 2.5rem;
    }
  }
  .samarbeidspartnere {
    margin-top: 20px;
  }
  hr {
    height: 3px;
    margin-bottom: 50px;
    background: var(--line-border-color);
    border:none;
  }
  .mt-5 {
    margin-top: 0px !important;
  }
</style>
