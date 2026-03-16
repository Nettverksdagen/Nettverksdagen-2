import Vue from 'vue'
import VueGtag from 'vue-gtag'

export default ({ router }) => {
  Vue.use(VueGtag, {
    config: {
      id: 'G-GPM81L23HM'
    }
  }, router)
}
