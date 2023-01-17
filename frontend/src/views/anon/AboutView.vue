<template>
  <div class="about-view">
    <Content>
      <h1>{{$t('about') + ' ' + $t('nettverksdagene')}}</h1>
      <b-row>
        <b-col cols="12" lg="6">
          <p class="introduction">
            {{$t('nettis')}}
            <br>
            <br>
            {{$t('inntektene')}}
          </p>
        </b-col>
        <b-col cols="12" lg="6" class="d-block d-sm-block">
          <b-img class="image" src="@/assets/excited_people.jpg" fluid alt="Engasjerte studenter i Glassgården"/>
        </b-col>
      </b-row>
    </Content>
  </div>
</template>

<script>
import Content from '@/components/common/Content.vue'
export default {
  name: 'AboutView',
  components: {
    Content
  }
}
</script>

<style lang="scss" scoped>
  .introduction {
    font-size:18px;
    text-align: center;
    @media(min-width: 768px) {
      text-align: left;
      margin-right: 30px;
    }
  }
  h1 {
    font-size: 36px;
    font-weight: 600;
    text-align: center;
    color: black;
    margin-bottom: 30px;
    margin-top: 40px;
    @media(min-width: 768px) {
      text-align: left;
    }
  }
  .image {
    border-style: solid;
    border: none;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 20px;
    margin-bottom: 20px;
    @media(min-width: 768px) {
      margin-top: 0px;
    }
  }
  .about-view {
      min-height: 80vh;
  }
</style>
