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
                        :options="allJobLocations">
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
            <Listing v-for="listing in filteredListings"
                     :key="listing.id"
                     :company="listing.company_name"
                     :title="listing.name"
                     :deadline="listing.deadline"
                     :logo-src="fileserverHost + '/thumb/512/' + listing.logo_uri"
                     :type="listing.type"
                     :listing-url="listing.listing_url"
                     :cities="listing.cities"
                     :internal-url="listing.internal_url"/>
          </b-list-group>
        </div>
      </b-row>
    </Content>
    <router-view />
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
      selectedJobLocations: [],
      windowWidth: 1000,
      filtersVisible: true
    }
  },
  computed: {
    availableListings: function () {
      let listings = this.$store.state.listings.all
      // Sort by id
      listings = listings.sort(function (a, b) {
        return a.id - b.id
      })

      // Convert cities string to array of cities
      listings = listings.filter(listing => {
        listing.cities = listing.city.split(',').map(city => city.trim())
        return listing
      })

      // Separate listings with and without deadline
      let listingsWithoutDeadline = listings.filter(listing => listing.deadline === null)
      listings = listings.filter(listing => listing.deadline !== null)

      Filter out old listings
      listings = listings.filter(
        listing => new Date(listing.deadline).setHours(0, 0, 0, 0) >= new Date().setHours(0, 0, 0, 0)
      )

      // Sort by deadline
      listings = listings.sort(function (a, b) {
        return new Date(a.deadline) - new Date(b.deadline)
      })

      // Spread out non-deadline listings evenly among the other listings
      listings = this.spread(listings, listingsWithoutDeadline)
      return listings
    },
    filteredListings: function () {
      let listings = this.availableListings
      // Filter out unchecked position types
      listings = listings.filter(listing => this.$data.selectedPositionTypes.indexOf(listing.type) !== -1)

      // Filter out unchecked job locations
      listings = listings.filter(listing => {
        let cityMatches = listing.cities.filter(city => this.$data.selectedJobLocations.indexOf(city) !== -1)
        return cityMatches !== undefined && cityMatches.length > 0
      })
      return listings
    },
    allJobLocations: function () {
      return this.sortByFrequencyAndRemoveDuplicates(
        [].concat.apply([], this.availableListings.map(listing => listing.cities))
      )
    }
  },
  mounted () {
    this.$options.allPositionTypes = this.sortByFrequencyAndRemoveDuplicates(
      this.$store.state.listings.all.map(listing => listing.type)
    )
    this.selectedPositionTypes = this.$options.allPositionTypes

    this.selectedJobLocations = this.allJobLocations
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
    },
    // Spreads the shorter array evenly among the elements of the longer array
    spread (a, b) {
      let shorter = []
      let longer = []
      if (a.length > b.length) {
        longer = a
        shorter = b
      } else {
        shorter = a
        longer = b
      }

      let totalLength = longer.length + shorter.length
      let freq = Math.ceil(totalLength / shorter.length)
      let res = []
      let i = 1
      while (longer.length > 0 || shorter.length > 0) {
        if (i % freq === 0 && shorter.length > 0) {
          res.push(shorter.shift())
        } else if (longer.length > 0) {
          res.push(longer.shift())
        }
        i++
      }
      return res
    }
  },
  watch: {
    allJobLocations: function (allJobLocations) {
      this.$data.selectedJobLocations = allJobLocations
    }
  }
}
</script>

<style lang="scss" scoped>
  .collapsed > .when-opened,
  :not(.collapsed) > .when-closed {
    display: none;
  }

  .listings {
    min-height: 80vh;
  }
</style>
