<template>
  <v-container fluid>
    <v-alert :value="error_msg != null" type="error">{{ error_msg }}</v-alert>
    <v-form>
      <v-container>
        <v-layout row wrap>
          <v-flex md12>
            <v-text-field
              class="stop-propagation"
              v-model="parcel_scan_info.tracking_id"
              label="物流单号"
              required
            ></v-text-field>
          </v-flex>
        </v-layout>
      </v-container>
    </v-form>
    <div>
      <v-card>
        <v-card-text>
          <p class="display-4 font-weight-black text-md-center">{{ sort_info.round_group_id }}</p>
          <v-text-field v-model="sort_info.weight" label="weight" :readonly="true"></v-text-field>
          <v-text-field
            v-model="sort_info.inbound_datetime"
            label="inbound datetime"
            :readonly="true"
          ></v-text-field>
        </v-card-text>
      </v-card>
    </div>
  </v-container>
</template>

<script>
import ParcelScanType from "@/mixins/ParcelScanType.vue";
export default {
  props: ["round_id", "job_id"],
  data: () => ({
    error_msg: null,
    sort_info: {
      round_group_id: null,
      weight: null,
      inbound_datetime: null
    }
  }),
  mounted: function() {},
  mixins: [ParcelScanType],
  methods: {
    getSortInfo: function() {
      var vm = this;
      vm.api.getParcelSortInfo(
        vm.parcel_scan_info.tracking_id,
        job_id,
        vm.round_id,
        resp => {
          vm.sort_info = resp.sort_info;
        },
        resp => {}
      );
    }
  },
  watch: {
    "parcel_scan_info.tracking_id": {
      handler: function(newValue, oldValue) {
        var vm = this;
        vm.getSortInfo();
      },
      deep: true
    }
  }
};
</script>

<style lang="scss">
</style>
