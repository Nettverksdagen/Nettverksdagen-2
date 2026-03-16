<template>
  <div :class="['home-box', { is_mobile: isMobile }]">
    <!-- <img src="@/assets/homebox.svg"> -->
    <img class="icon" :src="require(`@/assets/${boxIcon}`)" :alt="boxIconAlt">
    <div class="fancy-text">
      <h3>{{ boxTitle }}</h3>
      <h5 class="showme">{{ boxText }}</h5>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      windowWidth: window.innerWidth
    }
  },
  computed: {
    isMobile () {
      return this.windowWidth <= 768 // Same as breakpoints in CSS in HomeScreen.vue
    }
  },
  mounted () {
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.handleResize)
  },
  methods: {
    handleResize () {
      this.windowWidth = window.innerWidth
    }
  },
  props: ['boxIcon', 'boxIconAlt', 'boxTitle', 'boxText']
}
</script>

<style lang="scss" scoped>
  .home-box {
    overflow: hidden; // Prevents hover from outside the box
    height: 100%; // To stretch to fill parent
    background-color: rgb(245, 245, 246);
    border-radius: 1rem;
    padding: 1rem;

    // To move the text to the bottom of the box
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .fancy-text {
    display: flex;
    flex-direction: column;
    gap: calc(var(--font-size) / 2); // --font-size defined in the .boxes class
    transform: translateY(100%);
  }

  // Icon
  .icon {
    align-self: end; // To move the icon to the right side

    width: var(--icon-size); // --icon-size defined in the .boxes class
    height: var(--icon-size); // --icon-size defined in the .boxes class

    transition-duration: 400ms;
    filter: invert(20%) sepia(12%) saturate(2012%) hue-rotate(125deg) brightness(94%) contrast(94%);
  }

  .home-box:hover, .home-box.is_mobile {
    h3, .showme, .fancy-text {
      transition: opacity 300ms 200ms, transform 400ms; // Changing the transition times "reverses" the transition
      transform: translateY(0); // Transform trickery in order to animate the text appearing and disappearing
    }
    .showme {
      opacity: 1;
    }
    .icon{
      filter: invert(20%) sepia(12%) saturate(2012%) hue-rotate(125deg) brightness(130%) contrast(94%);
    }
  }
  h3 {
    transform: translateY(-100%);
    font-size: 125%; // Percentage of parent font size
    font-weight: 600;
    color: var(--primary-color); // --primary-color defined in App.vue
    word-break: break-all; // To break long words, shouldn't really be necessary
  }
  .showme {
    opacity: 0;

    font-size: 100%; // Percentage of parent font size
    color: var(--primary-color); // --primary-color defined in App.vue
    text-decoration: none;
  }
  h3, .showme, .fancy-text {
    margin-bottom: 0; // For some reason, headings have a default bottom margin
    transition: opacity 300ms, transform 400ms 150ms;
  }

</style>
