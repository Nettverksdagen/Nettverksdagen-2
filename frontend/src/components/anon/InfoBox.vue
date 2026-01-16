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
$medium-width: 768px;
.info-box {
  height: 100%;
  min-width: 100%;
  border-radius: 1rem;
  border-width: 3px;
  border-style: solid;
  border-color: var(--primary-color);
  background-color: var(--line-border-color);
  padding: 15px;
  margin-bottom: 5px;
}

.infoBoxHeading {
  font-size: 15px;
  font-weight: bold;
  color: var(--primary-color);
}

.infoBoxText {
  font-size: 14px;
  color: var(--primary-color);
  //overflow-wrap: break-word;
}

</style>