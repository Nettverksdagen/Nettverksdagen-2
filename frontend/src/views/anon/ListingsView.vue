<template>
  <div class="listings">
    <Content>
      <b-row>
        <div class="col-12 col-md-4">
          <b-card no-body class="mb-3" header="Filtre og sortering">
            <b-card-body class="pt-0">
              <b-btn v-b-toggle.filterCollapse variant="secondary" class="d-md-none w-100 mt-3">
                <span class="when-closed">Vis</span>
                <span class="when-opened">Skjul</span>
                filtre
              </b-btn>
              <b-collapse id="filterCollapse" class="mt-3" v-model="filtersVisible">
                <p class="text-secondary text-center">(Listen oppdateres automatisk)</p>
                <b-list-group>
                  <b-list-group-item>
                    <h4>Stillingstype</h4>
                    <b-form-group>
                      <b-form-checkbox-group
                        id="position-type-checkboxes"
                        v-model="selectedPositionTypes"
                        :options="$options.allPositionTypes">
                      </b-form-checkbox-group>
                    </b-form-group>
                  </b-list-group-item>
                </b-list-group>
              </b-collapse>
            </b-card-body>
          </b-card>
        </div>
        <div class="col-12 col-md-8">
          <b-list-group>
            <Listing v-for="listing in listings"
                     :key="listing.id"
                     :company="listing.company_name"
                     :title="listing.name"
                     :deadline="listing.deadline"
                     :logo-src="fileserverHost + '/' + listing.logo_uri"
                     :type="listing.type"
                     :listing-url="listing.listing_url"
                     :city="listing.city"/>
          </b-list-group>
        </div>
      </b-row>
    </Content>
  </div>
</template>

<script>
import Content from '@/components/common/Content.vue'
import Listing from '@/components/anon/Listing.vue'
export default {
  name: 'Listings',
  components: {
    Content,
    Listing
  },
  allPositionTypes: [],
  data () {
    return {
      fileserverHost: process.env.VUE_APP_FILESERVER_HOST,
      selectedPositionTypes: [],
      windowWidth: 1000,
      filtersVisible: true
    }
  },
  computed: {
    listings: function () {
      let listings = this.$store.state.listings.all
      // Filter out unchecked position types
      listings = listings.filter(listing => this.$data.selectedPositionTypes.indexOf(listing.type) !== -1)
      return listings
    }
  },
  mounted () {
    this.$options.allPositionTypes = this.$store.state.listings.all
      .map(listing => listing.type)
      .filter((listing, pos, listings) => {
        return listings.indexOf(listing) === pos
      })
    this.selectedPositionTypes = this.$options.allPositionTypes
  },
  created () {
    window.addEventListener('resize', this.handleResize)
    this.handleResize()
  },
  destroyed () {
    window.removeEventListener('resize', this.handleResize)
  },
  methods: {
    handleResize () {
      if (window.innerWidth >= 768) {
        this.filtersVisible = true
      } else {
        this.filtersVisible = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  .collapsed > .when-opened,
  :not(.collapsed) > .when-closed {
    display: none;
  }
</style>
