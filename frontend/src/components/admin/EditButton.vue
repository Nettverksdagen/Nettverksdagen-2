<template>
  <font-awesome-icon
    class="text-primary edit-button"
    :icon="{ prefix: 'fas', iconName: 'pencil-alt' }"
    size="lg"
    title="Endre"
  />
</template>

<script>
export default {
  name: 'EditButton'
}
</script>

<style scoped lang="scss">
.edit-button {
  cursor:pointer;
  opacity:0.8;
  transition:0.1s;
  &:hover {
    opacity:1;
  }
}
</style>
