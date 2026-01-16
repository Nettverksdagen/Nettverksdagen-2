<template>
  <div class="info-box" v-if="hasText">
    <h2 class="infoBoxHeading">{{ title }}</h2>
    <div v-if="paragraph" class="infoBoxText">
      {{paragraph}}
    </div>
    <p v-else class="text-gray-500 italic"></p>
  </div>
</template>

<script>
export default {
  name: "InfoBox",
  props: {
    title: {
      type: String,
      default: "" // Default to empty string if no title is provided
    },
    paragraph: {
      type: String,
      default: "" // Default to empty string if no paragraph is provided
    }
  },
  computed: {
    hasText() {
      return this.title.trim() || this.paragraph.trim()
    }
  }
};
</script>


<style scoped lang="scss">

.info-box {
  height: 100%;
  min-width: 100%;
  border-radius: 1rem;
  border-width: 2px;
  border-style: solid;
  border-color: var(--primary-color);
  background-color: var(--line-border-color);
  padding: 5px;
}

.infoBoxHeading {
  font-size: 20px;
  font-weight: bold;
  color: var(--primary-color);
}

.infoBoxText {
  color: var(--primary-color);
  //overflow-wrap: break-word;
}

</style>