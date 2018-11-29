<template>
  <div class="image-preview flex-grow-0" v-bind:class="{ 'show-preview': showImgPreview }">
    <b-img center fluid :src="imgPreviewSrc"></b-img>
  </div>
</template>

<script>
export default {
  name: 'ImageUploader',
  props: ['imgPreviewSrc', 'showImgPreview']
}
</script>

<style lang="scss" scoped>
.image-preview {
  width: 0;
  height: 100px;
  transition: width 0.4s;
  border-radius: 2px;
  margin:0;
  &.show-preview {
    width: 100px;
    margin-left: 1.2rem;
    img {
      opacity: 1 !important;
    }
  }
  img {
    opacity: 0 !important;
    transition: opacity 0.4s 0.4s;
  }
}
</style>
