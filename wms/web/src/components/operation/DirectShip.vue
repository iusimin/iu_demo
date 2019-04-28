<template>
  <v-container fluid>
    <v-alert :value="error_msg != null" type="error">{{ error_msg }}</v-alert>
    <v-form>
      <v-container>
        <v-layout row wrap>
          <v-flex md12>
            <v-text-field class="stop-propagation" v-model="parcel_scan_info.tracking_id" label="物流单号" required></v-text-field>
          </v-flex>
          <v-flex md12>
            <v-text-field class="stop-propagation" v-model="parcel_scan_info.weight" label="重量" required></v-text-field>
          </v-flex>
          <v-flex offset-md10 md2>
            <v-btn color="success" type="button" @click="submitDirectParcel">打单</v-btn>
          </v-flex>
        </v-layout>
      </v-container>
    </v-form>
  </v-container>
</template>

<script>
import ParcelScanListener from "@/mixins/ParcelScanListener.vue";
import ParcelScanType from "@/mixins/ParcelScanType.vue";
import Vue from "vue";

export default {
  data: () => ({
      error_msg: null,
      parcel_detail: null
  }),
  mixins: [ParcelScanListener, ParcelScanType],
  components: {},
  mounted: function() {},
  computed: {},
  methods: {
    submitDirectParcel: function() {},
    validateInput: function() {
      
    }
  },
  watch: {
    tracking_id: {
      handler: function(newValue, oldValue) {
        var vm = this;
        vm.parcel_scan_info.tracking_id = newValue;
      }
    },
    weight: {
      handler: function(newValue, oldValue) {
        var vm = this;
        vm.parcel_scan_info.weight = newValue;
      }
    }
  }
};
</script>

<style lang="scss">
</style>
