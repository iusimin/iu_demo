<template>
  <v-container fluid>
    <v-alert :value="error_msg != null" type="error">{{ error_msg }}</v-alert>
    <v-form>
      <v-container>
        <v-layout row wrap>
          <v-flex md12>
            <v-text-field id="TrackingIdInput" v-model="tracking_id" label="物流单号" required></v-text-field>
          </v-flex>
        </v-layout>
      </v-container>
    </v-form>
    <div>
      <v-text-field v-model="sort_info.weight" label="weight" :readonly="true"></v-text-field>
      <v-text-field v-model="sort_info.inbound_datetime" label="inbound datetime" :readonly="true"></v-text-field>
    </div>
  </v-container>
</template>

<script>
import ParcelScanType from "@/mixins/ParcelScanType.vue";
export default {
  props: ["sort_info"],
  data: () => ({
    error_msg: null
  }),
  mounted: function() {
    var vm = this;
    document
      .getElementById("TrackingIdInput")
      .addEventListener("keyup", vm.stopInputPropagation);
  },
  mixins: [ParcelScanType],
  methods: {
    stopInputPropagation: function(e) {
      e.stopPropagation();
    }
  },
  watch: {
    sort_info: {
      handler: function(newValue, oldValue) {
        var vm = this;
      },
      deep: true
    }
  },
  destroyed: function() {
    var vm = this;
    document
      .getElementById("TrackingIdInput")
      .removeEventListener("keyup", vm.stopInputPropagation);
  }
};
</script>

<style lang="scss">
</style>
