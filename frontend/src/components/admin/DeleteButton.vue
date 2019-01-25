<template>
  <font-awesome-icon
    class="text-danger delete-button"
    :icon="{ prefix: 'fas', iconName: 'trash-alt' }"
    size="lg"
    title="Slett"
  />
</template>

<script>
export default {
  name: 'DeleteButton'
}
</script>

<style scoped lang="scss">
.delete-button {
  cursor:pointer;
  opacity:0.8;
  transition:0.1s;
  &:hover {
    opacity:1;
  }
}
</style>
