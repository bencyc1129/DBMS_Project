<template>
  <InputQuery></InputQuery>
  <DropdownQuery></DropdownQuery>
</template>

<script>
import InputQuery from './components/InputQuery.vue'
import DropdownQuery from './components/DropdownQuery.vue'

export default {
  name: 'App',
  components: {
    InputQuery,
    DropdownQuery,
}
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
