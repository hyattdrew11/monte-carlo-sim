<template>
  <div id="app">
    <vue-progress-bar></vue-progress-bar>
    <HelloWorld />
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>

<style>
@import './assets/sass/style.scss'
</style>
