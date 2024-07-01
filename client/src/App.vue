<template>
  <NewLayout/>
</template>
<script setup lang="ts">
import NewLayout from './layouts/NewLayout.vue';

</script>
<style lang="scss">
  @import 'scss/main.scss';

  #app {
    font-family: 'Source Sans Pro', Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
  }
  body {
    margin: 0;
  }
  .va-dropdown__content.va-select-dropdown__content.va-dropdown__content-wrapper{
    z-index: 101!important;
  }
</style>
