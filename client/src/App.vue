<template>

  <router-view></router-view>
</template>

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

.pt-0 {
  padding-top: 0;
}

.p-0 {
  padding: 0;
}

.p-6 {
  padding: 6px;
}

.va-dropdown__content.va-select-dropdown__content.va-dropdown__content-wrapper {
  z-index: 101 !important;
}

.nav-h {
  height: 85px;
}

.row-equal .flex {
  .va-card {
    height: 100%;
  }
}

.flex-grow {
  flex-grow: 1;
}
</style>
