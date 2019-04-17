<template>
  <v-container fluid>
    <v-alert :value="error_msg != null" type="error">{{ error_msg }}</v-alert>
    <v-form>
      <v-container>
        <v-layout row wrap>
          <v-flex md12>
            <v-text-field id="TrackingIdInput" v-model="tracking_id" label="物流单号" required></v-text-field>
          </v-flex>
          <v-flex md12>
            <v-text-field id="WeightInput" v-model="weight" label="重量" required></v-text-field>
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
    //TODO: Refactor later
    var vm = this;
    document
      .getElementById("TrackingIdInput")
      .addEventListener("keyup", vm.stopInputPropagation);
    document
      .getElementById("WeightInput")
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
      .getElementById("TrackingIdInput")
      .removeEventListener("keyup", vm.stopInputPropagation);
    document
      .getElementById("WeightInput")
      .removeEventListener("keyup", vm.stopInputPropagation);
  }
}
</script>

<style lang="scss">
</style>
