<template>
  <v-container fluid>
    <v-stepper v-model="e6" vertical>
      <v-stepper-step :complete="e6 > 1" step="1">第一次分拣</v-stepper-step>

      <v-stepper-content step="1">
        <first-sort></first-sort>
        <v-btn color="primary" @click="e6 = 2">Continue</v-btn>
      </v-stepper-content>

      <v-stepper-step :complete="e6 > 2" step="2">第二次分拣</v-stepper-step>

      <v-stepper-content step="2">
        <second-sort></second-sort>
        <v-btn color="primary" @click="e6 = 3">Continue</v-btn>
      </v-stepper-content>

      <v-stepper-step :complete="e6 > 3" step="3">第三次分拣</v-stepper-step>

      <v-stepper-content step="3">
        <third-sort></third-sort>
      </v-stepper-content>

    </v-stepper>
  </v-container>
</template>

<script>
import FirstSort from "./FirstSort";
import SecondSort from "./SecondSort";
import ThirdSort from "./ThirdSort";

export default {
  data: () => ({
    e6: 1
  }),
  components: {
    FirstSort,
    SecondSort,
    ThirdSort
  }
}
</script>

<style lang="scss">
</style>
