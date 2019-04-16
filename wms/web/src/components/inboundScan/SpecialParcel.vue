<template>
  <v-container fluid>
    <v-alert :value="error_msg != null" type="error">{{ error_msg }}</v-alert>
    <v-form>
      <v-container>
        <v-layout row wrap>
          <v-flex md12>
            <v-text-field id="SpecialTrackingIdInput" v-model="tracking_id" label="物流单号" required></v-text-field>
          </v-flex>
          <v-flex md12>
            <v-text-field id="SpecialWeightInput" v-model="weight" label="重量" required></v-text-field>
          </v-flex>
          <v-flex md12>
            <v-checkbox v-model="has_battery" label="是否带电"></v-checkbox>
          </v-flex>
          <v-flex md12>
            <v-checkbox v-model="has_liquid" label="是否带液体"></v-checkbox>
          </v-flex>
        </v-layout>
      </v-container>
    </v-form>
  </v-container>
</template>

<script>
import ParcelScanType from "@/mixins/ParcelScanType.vue";
export default {
  data: () => ({
    error_msg: null
  }),
  mixins: [ParcelScanType],
  mounted: function() {
    var vm = this;
    document
      .getElementById("SpecialTrackingIdInput")
      .addEventListener("keyup", vm.stopInputPropagation);
    document
      .getElementById("SpecialWeightInput")
      .addEventListener("keyup", vm.stopInputPropagation);
  },
  methods: {
    stopInputPropagation: function(e) {
      e.stopPropagation();
    }
  },
  destroyed: function() {
    var vm = this;
    document
      .getElementById("SpecialTrackingIdInput")
      .removeEventListener("keyup", vm.stopInputPropagation);
    document
      .getElementById("SpecialWeightInput")
      .removeEventListener("keyup", vm.stopInputPropagation);
  }
}
</script>

<style lang="scss">
</style>
