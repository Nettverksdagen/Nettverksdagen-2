<template>
  <div class="not-found-view">
    <Content>
      <b-row class="row justify-content-center">
        <b-col cols="12" lg="6">
          <h1>Oisann! Den siden finnes ikke</h1>
          <p class="desc">
            Sjekk at du har stavet addressen riktig, eller gå tilbake til <router-link to="/">hjemmesiden</router-link>.
          </p>
        </b-col>
        <b-col cols="6" lg="3" class="d-block d-sm-block">
          <b-img class="image" src="@/assets/logo.png" fluid alt="Nettverksdagene logo"/>
        </b-col>
      </b-row>
    </Content>
  </div>
</template>

<script>
import Content from '@/components/common/Content.vue'
export default {
  name: 'NotFoundView',
  components: {
    Content
  }
}
</script>

<style lang="scss" scoped>
  .desc {
    font-size: 24px;
    text-align: center;
    @media(min-width: 768px) {
      font-size: 30px;
    }
  }
  h1 {
    font-size: 30px;
    font-weight: 600;
    text-align: center;
    color: black;
    margin-bottom: 30px;
    margin-top: 40px;
    @media(min-width: 768px) {
      font-size: 42px;
    }
  }
  .image {
    border-style: solid;
    border: none;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 20px;
    margin-bottom: 20px;
    width: 60%;
    display: none;
    margin: auto;
    @media(min-width: 768px) {
      margin-top: 0px;
      display: block;
    }
  }
  .about-view {
      min-height: 80vh;
  }
</style>
