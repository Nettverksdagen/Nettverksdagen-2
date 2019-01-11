<template>
  <div class="listings">
    <Content>
      <b-row>
        <div class="col-12 col-md-4">
          <b-card no-body class="mb-3" header="Filtrer annonser">
            <b-card-body class="pt-0">
              <b-btn v-b-toggle.filterCollapse variant="secondary" class="d-md-none w-100 mt-3">
                <span class="when-closed">Vis</span>
                <span class="when-opened">Skjul</span>
                filter
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

                  <b-list-group-item>
                    <h4>Sted</h4>
                    <b-form-group>
                      <b-form-checkbox-group
                        id="job-location-checkboxes"
                        v-model="selectedJobLocations"
                        :options="$options.allJobLocations">
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
  allJobLocations: [],
  data () {
    return {
      fileserverHost: process.env.VUE_APP_FILESERVER_HOST,
      selectedPositionTypes: [],
      selectedJobLocations: [],
      windowWidth: 1000,
      filtersVisible: true
    }
  },
  computed: {
    listings: function () {
      let listings = this.$store.state.listings.all
      // Filter out unchecked position types
      listings = listings.filter(listing => this.$data.selectedPositionTypes.indexOf(listing.type) !== -1)

      // Filter out unchecked job locations
      listings = listings.filter(listing => this.$data.selectedJobLocations.indexOf(listing.city) !== -1)

      // Filter out old listings
      listings = listings.filter(listing => new Date(listing.deadline) > new Date())

      // Sort by deadline
      listings = listings.sort(function (a, b) {
        return new Date(a.deadline) - new Date(b.deadline)
      })
      return listings
    }
  },
  mounted () {
    this.$options.allPositionTypes = this.sortByFrequencyAndRemoveDuplicates(
      this.$store.state.listings.all.map(listing => listing.type)
    )
    this.selectedPositionTypes = this.$options.allPositionTypes

    this.$options.allJobLocations = this.sortByFrequencyAndRemoveDuplicates(
      this.$store.state.listings.all.map(listing => listing.city)
    )
    this.selectedJobLocations = this.$options.allJobLocations
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
      this.filtersVisible = window.innerWidth >= 768
    },
    sortByFrequencyAndRemoveDuplicates (arr) {
      // Obtain array of unique elements
      let uniques = arr.filter((elem, pos, arr) => {
        return arr.indexOf(elem) === pos
      })

      // Create empty object of frequencies initialized at zero
      let frequencies = {}
      for (let i = 0; i < uniques.length; i++) {
        frequencies[uniques[i]] = 0
      }

      // Compute the frequencies
      for (let i = 0; i < arr.length; i++) {
        frequencies[arr[i]]++
      }

      // Return unique array sorted by frequency (most common first)
      return uniques.sort(function (a, b) {
        return frequencies[b] - frequencies[a]
      })
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
