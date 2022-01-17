<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'babel-polyfill'
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text-primary-color);
  background:var(--background-color-primary);
  min-height:100vh;
  transition: background 0.5s;
  transition: color 0.5s;
}
:root {
  --background-color-primary: #ffffff;
  --text-primary-color: #222;
  --header-text-color: #1F4945;
  --header-text-secondary-color: #dadce0;
  --line-border-color: #dadce0;
  --slider-color: #dadce0;
}
:root.dark-theme {
  --background-color-primary: #202124;
  --text-primary-color: #ddd;
  --header-text-color: #98989a;
  --header-text-secondary-color: #5f6368;
  --line-border-color: #5f6368;
  --slider-color: #5f6368;
}
</style>
