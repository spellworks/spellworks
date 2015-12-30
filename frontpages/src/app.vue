<template lang="jade">
  #app
    img.logo(src="./assets/logo.png")
    hello
</template>

<script>
import hello from './components/hello'

export default {
  components: {
    hello
  }
}
</script>

<style>
body {
  font-family: Helvetica, sans-serif;
}
</style>
