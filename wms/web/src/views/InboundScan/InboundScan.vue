<template>
  <v-container fluid>
    <v-tabs centered color="cyan" dark icons-and-text>
      <v-tabs-slider color="yellow"></v-tabs-slider>

      <v-tab href="#tab-1">
        普货入库
        <v-icon>普货</v-icon>
      </v-tab>
      <v-tab href="#tab-2">
        特货入库
        <v-icon>特货</v-icon>
      </v-tab>
      <v-tab href="#tab-3">
        敏感货物入库
        <v-icon>敏感货物</v-icon>
      </v-tab>

      <v-tab-item value="tab-1">
        <ordinary-parcel></ordinary-parcel>
      </v-tab-item>
      <v-tab-item value="tab-2">
        <special-parcel></special-parcel>
      </v-tab-item>
      <v-tab-item value="tab-3">
        <sensitive-parcel></sensitive-parcel>
      </v-tab-item>
    </v-tabs>
  </v-container>
</template>

<script>
import OrdinaryParcel from "./OrdinaryParcel";
import SpecialParcel from "./SpecialParcel";
import SensitiveParcel from "./SensitiveParcel";

export default {
  data: () => ({
    typography: {}
  }),
  components: {
    OrdinaryParcel,
    SpecialParcel,
    SensitiveParcel
  }
}
</script>

<style lang="scss">
</style>
