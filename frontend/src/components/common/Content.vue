<template>
  <div class="content flex-grow-1">
    <div class="wrapper">
      <slot></slot>
    </div>
  </div>
</template>

<script>
</script>

<style lang="scss" scoped>
  .content {
    margin: 15px 15px;
    @media (min-width: 992px) {
      margin: 20px 15px;
    }
    @media (min-width: 1200px) {
      margin: 20px 100px;
    }
    @media (min-width: 1400px) {
      margin: 30px 200px;
    }
  }
  a {
    color: #187c79;
  }
</style>
